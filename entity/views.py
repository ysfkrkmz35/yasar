# Merged File: views.py

from django.shortcuts import render, get_object_or_404,redirect,render
from django.contrib.auth.decorators import login_required
from .models import Unit, Employee, Group, MemberGroup
from django.http import HttpResponseForbidden

def unit_hierarchy(request, unit_id=None):
    # Eğer bir unit_id varsa, ilgili birimi getir, yoksa üst düzey birimleri göster.
    if unit_id:
        unit = get_object_or_404(Unit, id=unit_id)
        sub_units = Unit.objects.filter(parent_unit=unit)
        employees = Employee.objects.filter(unit=unit)

    else:
        unit = None
        sub_units = Unit.objects.filter(parent_unit__isnull=True)
        employees = Employee.objects.filter(unit__isnull=True)  # unit alanı boş olanlar

    return render(request, 'yasar/unit_hierarchy.html', {
        'unit': unit,
        'sub_units': sub_units,
        'employees': employees,
    })

#group view
@login_required
def create_group(request):
    if not request.user.employee.can_create_group:
        return HttpResponseForbidden("Bu işlem için yetkiniz yok.")

    error_message = None

    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        description = request.POST.get('description')

        # Grup isminin benzersiz olduğunu kontrol et
        if Group.objects.filter(name=group_name).exists():
            error_message = "Bu isimde bir grup zaten mevcut. Lütfen farklı bir isim seçin."
        else:
            # Yeni grup oluştur
            group = Group.objects.create(name=group_name, description=description)

            # Grup üyelerini ve rollerini al
            employees = request.POST.getlist('employees')  # Çalışan ID'leri
            roles = request.POST.getlist('roles')  # Rol bilgileri

            for employee_id, role in zip(employees, roles):
                employee = Employee.objects.get(id=employee_id)
                MemberGroup.objects.create(member=employee, group=group, role_in_group=role)

            return redirect('/view_groups/')

    employees = Employee.objects.all()
    role_choices = MemberGroup.ROLE_CHOICES  # Rol seçeneklerini modelden al
    return render(request, 'yasar/create_group.html', {'employees': employees, 'role_choices': role_choices, 'error_message': error_message})



@login_required
def view_groups(request):
    if not hasattr(request.user, 'employee'):
        return HttpResponseForbidden("Bu işlem için bir çalışan hesabına sahip olmanız gerekiyor.")

    if request.user.is_superuser or request.user.employee.can_create_group:
        # Grup oluşturma yetkisi olanlar tüm grupları görür
        groups = Group.objects.prefetch_related('members__member').all()
    else:
        # Kullanıcı sadece üyesi olduğu grupları görür
        member_groups = MemberGroup.objects.filter(member=request.user.employee)
        groups = Group.objects.filter(id__in=member_groups.values_list('group_id', flat=True)) \
            .prefetch_related('members__member')

    return render(request, 'yasar/view_groups.html', {'groups': groups})



    #group view son


def index(request):
    employee = getattr(request.user, 'employee', None)
    if employee:
        user_can_create_report = MemberGroup.objects.filter(member=employee, can_create_report=True).exists()
    else:
        user_can_create_report = False

    return render(request, 'yasar/index.html', {'user_can_create_report': user_can_create_report})

# From Meetings Folder:

from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden,HttpResponseRedirect
from weasyprint import HTML
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Meeting,Attendants,Decisions, Topics
from entity.models import Unit,Employee, Group, MemberGroup
from .forms import AttendantForm, DecisionForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q
from datetime import datetime, timedelta
from django.urls import reverse



@login_required
def create_meeting(request):
    # Kullanıcının MemberGroup'larındaki toplantı oluşturma yetkisini kontrol et
    employee = getattr(request.user, 'employee', None)
    if not employee or not MemberGroup.objects.filter(member=employee, can_create_report=True).exists():
        return HttpResponseForbidden("Bu işlem için yetkiniz yok.")

    if request.method == "POST":
        meeting_name = request.POST.get("meeting_name")
        date = request.POST.get("date")
        parent_meeting_id = request.POST.get("parent_meeting")

        # Parent toplantı kontrolü
        parent_meeting = None
        if parent_meeting_id:
            try:
                parent_meeting = Meeting.objects.get(id=parent_meeting_id)
            except Meeting.DoesNotExist:
                parent_meeting = None

        # Yeni toplantı oluşturma
        if meeting_name and date:
            meeting = Meeting.objects.create(
                meeting_name=meeting_name,
                date=date,
                created_by=request.user.employee,
                parent_meeting=parent_meeting
            )
            return redirect('add_attendants_decisions', meeting_id=meeting.id)

    # Mevcut tüm toplantıları alın
    meetings = Meeting.objects.all()

    return render(request, 'yasar/create_meeting.html', {
        'meetings': meetings
    })

@login_required
def view_meetings(request):
    # Tüm toplantıları al
    if request.user.is_superuser:
        all_meetings = Meeting.objects.prefetch_related('attendants__member', 'decisions__responsible')
    else:
        # Kullanıcının katıldığı toplantıları al
        user_employee = request.user.employee
        all_meetings = Meeting.objects.filter(
            attendants__member=user_employee
        ).prefetch_related('attendants__member', 'decisions__responsible')

    # Arama kriterlerini al
    meeting_name_query = request.GET.get('meeting_name', '')
    start_date_query_str = request.GET.get('start_date', '')
    end_date_query_str = request.GET.get('end_date', '')

    # Tarih aralığını saatlerle düzenle
    start_date_query = None
    end_date_query = None
    if start_date_query_str:
        start_date_query = datetime.strptime(start_date_query_str, '%Y-%m-%d')
    if end_date_query_str:
        # Bitiş tarihinin son anına kadar dahil edilmesi için 1 gün eklenir
        end_date_query = datetime.strptime(end_date_query_str, '%Y-%m-%d') + timedelta(days=1)

    # Eğer arama kriterleri varsa; hem parent hem child kayıtları kapsayacak Q nesnesi oluşturun.
    if meeting_name_query or start_date_query or end_date_query:
        q = Q()
        if meeting_name_query:
            q &= Q(meeting_name__icontains=meeting_name_query) | Q(meeting__meeting_name__icontains=meeting_name_query)
        if start_date_query:
            q &= Q(date__gte=start_date_query) | Q(meeting__date__gte=start_date_query)
        if end_date_query:
            q &= Q(date__lt=end_date_query) | Q(meeting__date__lt=end_date_query)

        # Filtreyi tüm toplantılar üzerine uygulayın.
        search_results = all_meetings.filter(q).distinct()

        return render(request, 'yasar/view_meetings.html', {
            'meetings': search_results,
            'meeting_name_query': meeting_name_query,
            'start_date_query': start_date_query_str,
            'end_date_query': end_date_query_str,
            'search_mode': True,
        })

    # Arama yapılmamışsa; tüm toplantıları gönderin.
    return render(request, 'yasar/view_meetings.html', {
        'meetings': all_meetings,
        'meeting_name_query': meeting_name_query,
        'start_date_query': start_date_query_str,
        'end_date_query': end_date_query_str,
        'search_mode': False,
    })

#attendant, decision ekleme ekranı---------------------------------------------------------------------------------------------

@csrf_exempt
def add_attendants_decisions(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    attendants = Attendants.objects.filter(meeting=meeting)
    decisions = Decisions.objects.filter(meeting=meeting)
    employees = Employee.objects.all()
    groups = Group.objects.all()
    topics = Topics.objects.filter(meeting=meeting)

    return render(request, 'yasar/add_attendants_decisions.html', {
        'meeting': meeting,
        'attendants': attendants,
        'decisions': decisions,
        'employees': employees,
        'groups': groups,
        'topics': topics,
    })

@csrf_exempt
def upload_meeting_file(request, meeting_id):
    """
    Toplantıya dosya yükleme işlemini gerçekleştirir.
    """
    meeting = get_object_or_404(Meeting, id=meeting_id)

    if request.method == "POST" and request.FILES.get('meeting_file'):
        meeting.meeting_file = request.FILES['meeting_file']
        meeting.save()
        return HttpResponseRedirect(reverse('add_attendants_decisions', args=[meeting_id]))

    return JsonResponse({'success': False, 'error': 'Dosya yükleme başarısız oldu.'}, status=400)

@csrf_exempt
def add_attendant(request, meeting_id):
    if request.method == "POST":
        member_id = request.POST.get("member_id")
        group_id = request.POST.get("group_id")
        meeting = get_object_or_404(Meeting, id=meeting_id)

        if group_id:
            group = get_object_or_404(Group, id=group_id)
            for member_group in group.members.all():
                Attendants.objects.get_or_create(meeting=meeting, member=member_group.member)
        elif member_id:
            Attendants.objects.get_or_create(meeting=meeting, member_id=member_id)

        return HttpResponseRedirect(reverse('add_attendants_decisions', args=[meeting_id]))


@csrf_exempt
def delete_attendant(request, attendant_id):
    if request.method == "POST":
        try:
            attendant = Attendants.objects.get(id=attendant_id)
            meeting_id = attendant.meeting.id
            attendant.delete()
        except Attendants.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse('add_attendants_decisions', args=[meeting_id]))



@csrf_exempt
def add_decision(request, meeting_id):
    if request.method == "POST":
        meeting = get_object_or_404(Meeting, id=meeting_id)
        decision_text = request.POST.get("decision_text")
        topic_group = request.POST.get("topic_group")
        decision_status = request.POST.get("decision_status")  # Durum alınır
        responsible_id = request.POST.get("responsible")
        topic_id = request.POST.get("meeting_topic")

        responsible = None
        if responsible_id:
            responsible = Employee.objects.get(id=responsible_id)

        topic = None
        if topic_id:
            topic = Topics.objects.get(id=topic_id)

        if decision_status not in ['finalized', 'pending', 'cancelled']:
            return JsonResponse({'error': 'Geçersiz karar durumu!'}, status=400)

        # Kararı oluştur
        decision = Decisions.objects.create(
            meeting=meeting,
            decision_text=decision_text,
            topic_group=topic_group,
            decision_status=decision_status,
            responsible=responsible,
            meeting_topic=topic
        )

        return HttpResponseRedirect(reverse('add_attendants_decisions', args=[meeting_id]))

@csrf_exempt
def delete_decision(request, decision_id):
    if request.method == "POST":
        try:
            decision = Decisions.objects.get(id=decision_id)
            meeting_id = decision.meeting.id
            decision.delete()
        except Decisions.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse('add_attendants_decisions', args=[meeting_id]))


@csrf_exempt
def add_topic_to_meeting(request, meeting_id):
    if request.method == "POST":
        topic_text = request.POST.get("topic_text")
        meeting = get_object_or_404(Meeting, id=meeting_id)

        if topic_text:
            Topics.objects.create(meeting=meeting, topic_text=topic_text)

        return HttpResponseRedirect(reverse('add_attendants_decisions', args=[meeting_id]))


@csrf_exempt
def delete_topic(request, topic_id):
    if request.method == "POST":
        try:
            topic = Topics.objects.get(id=topic_id)
            meeting_id = topic.meeting.id
            topic.delete()
        except Topics.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse('add_attendants_decisions', args=[meeting_id]))


@login_required
def get_group_members(request):
    group_id = request.GET.get('group_id')
    try:
        group = get_object_or_404(Group, id=group_id)
        members = [
            {
                "id": member.member.id,
                "name": f"{member.member.first_name} {member.member.last_name}"
            }
            for member in group.members.all()
        ]
        return JsonResponse({"success": True, "members": members})
    except Group.DoesNotExist:
        return JsonResponse({"success": False, "error": "Grup bulunamadı."}, status=404)

@csrf_exempt
def add_group_to_meeting(request, meeting_id):
    """
    Belirli bir gruba ait tüm üyeleri toplantıya katılımcı olarak ekler.
    """
    if request.method == "POST":
        group_id = request.POST.get('group_id')  # Formdan gelen 'group_id'

        if not group_id:
            return JsonResponse({'success': False, 'error': 'Grup ID belirtilmedi.'}, status=400)

        meeting = get_object_or_404(Meeting, id=meeting_id)
        group = get_object_or_404(Group, id=group_id)

        # Grubun tüm üyelerini katılımcı olarak ekle
        for member_group in group.members.all():
            Attendants.objects.get_or_create(meeting=meeting, member=member_group.member)

        return HttpResponseRedirect(reverse('add_attendants_decisions', args=[meeting_id]))

    return JsonResponse({'success': False, 'error': 'Bu endpoint yalnızca POST isteklerini kabul eder.'}, status=405)



@csrf_exempt
@login_required
def cancel_meeting(request, meeting_id):
    if request.method == "POST":
        meeting = get_object_or_404(Meeting, id=meeting_id)

        if request.user.employee != meeting.created_by and not request.user.is_superuser:
            return JsonResponse({'success': False, 'error': 'Bu toplantıyı iptal etme yetkiniz yok!'}, status=403)

        Attendants.objects.filter(meeting=meeting).delete()
        Decisions.objects.filter(meeting=meeting).delete()
        meeting.delete()

        return HttpResponseRedirect(reverse('index'))  # Ana sayfaya yönlendirme

#attendant, decision ekleme ekranı son---------------------------------------------------------------------------------------------

#meeting bilgielrini pdf formatında indirme


def generate_meeting_pdf(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    attendants = meeting.attendants.all()
    decisions = meeting.decisions.all()

    # Şablon oluşturma
    html_string = render_to_string('yasar/meeting_pdf_template.html', {
        'meeting': meeting,
        'attendants': attendants,
        'decisions': decisions,
    })

    # PDF yanıtı oluşturma
    response = HttpResponse(content_type='application/pdf')

    # İstek kaynağına göre içerik düzenleme
    if 'generate-meeting-pdf' in request.path:
        response['Content-Disposition'] = f'inline; filename="meeting_{meeting.id}.pdf"'
    else:
        response['Content-Disposition'] = f'attachment; filename="meeting_{meeting.id}.pdf"'

    HTML(string=html_string).write_pdf(response)
    return response


#kararlar ekranı
@login_required
def view_decisions(request):
    # Superuser için tüm kararlar
    if request.user.is_superuser:
        decisions = Decisions.objects.select_related('meeting', 'responsible').all()
    else:
        # Kullanıcı yalnızca katıldığı toplantılardaki kararları görebilir
        attended_meetings = Attendants.objects.filter(member=request.user.employee).values_list('meeting_id', flat=True)
        decisions = Decisions.objects.select_related('meeting', 'responsible').filter(meeting_id__in=attended_meetings)

    # Arama kriterlerini al
    topic_group_query = request.GET.get('topic_group', '')
    responsible_first_name_query = request.GET.get('responsible_first_name', '')
    responsible_last_name_query = request.GET.get('responsible_last_name', '')
    meeting_name_query = request.GET.get('meeting_name', '')
    date_query = request.GET.get('date', '')

    # Arama kriterlerini uygula
    if topic_group_query:
        decisions = decisions.filter(topic_group__icontains=topic_group_query)

    if responsible_first_name_query:
        decisions = decisions.filter(responsible__first_name__icontains=responsible_first_name_query)

    if responsible_last_name_query:
        decisions = decisions.filter(responsible__last_name__icontains=responsible_last_name_query)

    if meeting_name_query:
        decisions = decisions.filter(meeting__meeting_name__icontains=meeting_name_query)

    if date_query:
        decisions = decisions.filter(meeting__date__date=date_query)

    # Kararları durumlarına göre ayır
    pending_decisions = decisions.filter(decision_status='pending')
    finalized_decisions = decisions.filter(decision_status__in=['finalized', 'completed_later'])
    cancelled_decisions = decisions.filter(decision_status__in=['cancelled', 'cancelled_later'])

    # Her karar için ek bilgi ekle
    def decision_with_extra(decision):
        # Kullanıcının bu kararı güncelleme yetkisini kontrol et
        can_update = (
            request.user.is_superuser or
            Attendants.objects.filter(meeting=decision.meeting, member=request.user.employee).exists()
        )
        return {
            'decision': decision,
            'can_update': can_update
        }

    pending_decisions_with_extra = [decision_with_extra(d) for d in pending_decisions]
    finalized_decisions_with_extra = [decision_with_extra(d) for d in finalized_decisions]
    cancelled_decisions_with_extra = [decision_with_extra(d) for d in cancelled_decisions]

    return render(request, 'yasar/view_decisions.html', {
        'pending_decisions_with_extra': pending_decisions_with_extra,
        'finalized_decisions_with_extra': finalized_decisions_with_extra,
        'cancelled_decisions_with_extra': cancelled_decisions_with_extra,
    })


@login_required
def update_decision(request, decision_id):
    decision = get_object_or_404(Decisions, id=decision_id)

    # Yalnızca süper kullanıcılar veya kararın bağlı olduğu toplantının yöneticisi/raportörü erişebilir
    if not (request.user.is_superuser or
            decision.meeting.attendants.filter(member=request.user.employee, role_in_group__in=['Yönetici', 'Raportör']).exists()):
        return HttpResponseForbidden("Bu işlemi yapma yetkiniz yok.")

    if request.method == 'POST':
        finished_date = request.POST.get('finished_date')
        finish_text = request.POST.get('finish_text')
        evidence_file = request.FILES.get('evidence_file')
        decision_status = request.POST.get('decision_status')

        if decision_status not in ['completed_later', 'cancelled_later']:
            return JsonResponse({'error': 'Geçersiz karar durumu!'}, status=400)

        decision.decision_status = decision_status
        decision.decision_finished_date = finished_date
        decision.decision_finish_text = finish_text
        if evidence_file:
            decision.evidence_file = evidence_file
        decision.save()
        return redirect('view_decisions')

    return render(request, 'yasar/update_decision.html', {
        'decision': decision,
    })

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django import forms

from django.contrib.auth.models import User
from django.db.models import Q

from system.load import load_prms

from entity.models import Employee

from .entity_forms import EmployeeFilterRequestForm, EmployeeForm

from .templatetags.yasar_filters import is_emp_sup, is_emp_mgr

from .member import adjust_phone_fields, check_phone_number

@login_required(login_url='/login/')
def index(request):
    # Load PRMS
    PRMS = load_prms(request)

    if not is_emp_sup(request.user):
        return HttpResponse('Çalışanları listeleme yetkiniz yok.')

    page_no_reset = False

    # The request is posted back
    if request.method == 'POST':
        form = EmployeeFilterRequestForm(request.POST)
    else:
        form = EmployeeFilterRequestForm(initial={'member':PRMS['DEF_EMP']})

    form.fields['member'].widget = forms.TextInput()

    if request.method == 'POST':
        if not form.is_valid():
            return HttpResponse('Invalid response from Employee Index edit page. Please go back and enter valid data.' + form.as_p())

        new_default = form.cleaned_data['member']

        if new_default != PRMS['DEF_EMP']:
            PRMS['DEF_EMP'] = new_default
            PRMS['EMPS_PAG_NO'] = 1
            page_no_reset = True
            request.session['PRMS'] = PRMS
            request.session.modified = True

    if PRMS['DEF_EMP'] != '':
        employees = Employee.objects.filter(Q(first_name__icontains=PRMS['DEF_EMP'])|Q(last_name__icontains=PRMS['DEF_EMP']))
    else:
        employees = Employee.objects.all()

    if page_no_reset:
        page_no = 1
    else:
        page = request.GET.get('page')

        if page is not None:
            page_no = int(page)
        else:
            page_no = PRMS['EMPS_PAG_NO']

        if page_no != PRMS['EMPS_PAG_NO']:
            PRMS['EMPS_PAG_NO'] = page_no
            request.session['PRMS'] = PRMS
            request.session.modified = True

    paginator = Paginator(employees, PRMS['RCD_PER_PAG'])  # Limits authors per page.

    page_obj = paginator.get_page(page_no)

    employee_context = {'form':form, 'employeers': employees, 'PRMS': PRMS, 'page_obj': page_obj}

    return render(request, 'yasar/employee_index.html', employee_context)

login_required(login_url='/login/')
def manage(request):
    # Load PRMS
    PRMS = load_prms(request)

    if not is_emp_sup(request.user):
        return HttpResponse('Çalışan bilgilerine ulaşma yetkiniz yok.')

    # Initialize parameters
    action = request.GET.get('action')

    if (action != 'CREATE') and (action != 'EDIT') and (action != 'VIEW'):
        return HttpResponse('Tanımlanmamış işlem: ' + str(action))

    if action is None:
        action = 'VIEW'

    if action == 'CREATE':
        if not is_emp_mgr(request.user):
            return HttpResponse('Çalışan ekleme yetkiniz yok.')

        allowed_users = User.objects.filter(~Q(first_name__exact="") & ~Q(last_name__exact=""))

        usr_options = ()
        for user in allowed_users:
            usr_options += ((user.id, user.last_name+', '+user.first_name),)
    else:
        if action == 'EDIT' and not is_emp_mgr(request.user):
                return HttpResponse('Çalışan bilgilerini düzenleme yetkiniz yok.')

        employee_id_str = request.GET.get('employee_id')

        if employee_id_str is None:
            return HttpResponse('Employee id not specified.')

        member = Employee.objects.get(pk=int(employee_id_str))

    # The request is posted back to create and/or save an Author
    if request.method == 'POST':
        if action == 'CREATE':
            form = EmployeeForm(request.POST)
            form.fields['user'].choices = usr_options
            form.fields['user'].widget.choices = usr_options
        else:
            form = EmployeeForm(request.POST, instance=member)

        if form.is_valid():
            (is_phone_valid, err_msg) = check_phone_number(form)

            if not is_phone_valid:
                return HttpResponse(err_msg)

            employee = form.save()
            return HttpResponseRedirect('/yasar/employee_manage?action=VIEW&employee_id='+str(employee.id))

        if action == 'CREATE':
            return HttpResponse('Invalid response from employee create page. Please go back and enter valid data. ' + form.as_p())
        else:
            return HttpResponse('Invalid response from employee edit page. Please go back and enter valid data. ' + form.as_p())
    else:
        if action == 'CREATE':
            form = EmployeeForm()
            form.fields['user'].choices = usr_options
            form.fields['user'].widget.choices = usr_options
            adjust_phone_fields(form)
            employee_context = {'action':action, 'form':form, 'PRMS': PRMS, 'member_type':PRMS['EMP_MEMBER']}
        elif action == 'EDIT':
            form = EmployeeForm(instance=member)
            adjust_phone_fields(form)
            employee_context = {'action':action, 'form':form, 'member':member, 'PRMS': PRMS, 'member_type':PRMS['EMP_MEMBER']}
        else:
            employee_context = {'action':action, 'member':member, 'PRMS': PRMS, 'member_type':PRMS['EMP_MEMBER']}

    return render(request, 'yasar/employee_manage.html', employee_context)


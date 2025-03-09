# Merged File: models.py

import re

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from django.db.models import Q

from django.db.models.signals import pre_save
from django.dispatch import receiver

from system.params import PRMS

from .validators import author_name_validator, product_name_validator
from .validators import phone_country_validator, phone_part2_validator, phone_part4_validator

# All models in the application. Check the signals below models.

# All base and inherited user models.

class Unit(models.Model):
    id = models.AutoField('No', primary_key=True,)
    name = models.CharField('Ad', max_length=64, unique=True, blank=False, null=False)
    parent_unit=models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Birim'
        verbose_name_plural = 'Birimler'



class Member(models.Model):
    id = models.AutoField(primary_key=True,)
    user = models.OneToOneField(User, verbose_name='Kullanıcı', on_delete=models.CASCADE,)
    first_name = models.CharField('Adı', max_length=32, blank=False, null=False, default='TempName')
    last_name = models.CharField('Soyadı', max_length=32, blank=False, null=False, default='TempSurname')
    phone_country = models.CharField('Telefon Ülke Codu', max_length=3, blank=True, null=True, validators=phone_country_validator)
    phone_part2 = models.CharField('Telefon (2. Parça)', max_length=3, blank=True, null=True, validators=phone_part2_validator)
    phone_part3 = models.CharField('Telefon (3. Parça)', max_length=3, blank=True, null=True, validators=phone_part2_validator)
    phone_part4 = models.CharField('Telefon (4. Parça)', max_length=4, blank=True, null=True, validators=phone_part4_validator)
    role = models.CharField('Yetkinlik', max_length=8, choices=PRMS['AUT_LVLS'], default=PRMS['DEF_AUT_LVL'])
    title = models.CharField('Ünvan', max_length = 25, blank = False , null = False, default = 'Çalışan')
    unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.SET_NULL, related_name='employees')
    can_create_group = models.BooleanField('Grup Oluşturma Yetkisi', default=False)

    # Properties for cloned fields

    def long_name(self):
        return self.first_name + ' ' + self.last_name
    long_name.short_description = 'Adı ve Soyadı'

    def list_name(self):
        return self.last_name + ', ' + self.first_name
    list_name.short_description = 'Soyadı, Adı'

    def phone_number(self):
        return '+' + self.phone_country + self.phone_part2 + self.phone_part3 + self.phone_part4
    list_name.short_description = 'Soyadı, Adı'

    def is_active(self):
        return self.user.is_active
    is_active.short_description = 'Etkin'

    def employee_unit(self):
        return self.unit
    list_name.short_description = 'Çalıştığı bölüm'

    def __str__(self):
        return self.list_name()

    class Meta:
        abstract = True
        ordering = ['last_name','first_name',]
        unique_together = ('first_name', 'last_name',)


class Employee(Member):
    pass


    class Meta(Member.Meta):
        verbose_name = 'Çalışan'
        verbose_name_plural = 'Çalışanlar'
        constraints = [models.CheckConstraint(name="employee_empty_first_and_last_name", check=(~Q(first_name__exact="") & ~Q(last_name__exact="")))]



# group models
class Group(models.Model):
    id = models.AutoField(primary_key=True)  # ID alanı tanımlı
    name = models.CharField('Grup Adı', max_length=64, unique=True)  # Grup adı unique olarak bırakıldı
    description = models.TextField('Açıklama', blank=True, null=True)
    created_at = models.DateTimeField('Oluşturulma Tarihi', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Grup'  # Tekil isim
        verbose_name_plural = 'Gruplar'  # Çoğul isim


class MemberGroup(models.Model):
    id = models.AutoField(primary_key=True)  # ID alanı tanımlı
    ROLE_CHOICES = [
        ('Yönetici', 'Yönetici'),
        ('Raportör', 'Raportör'),
        ('Üye', 'Üye'),
    ]

    member = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='groups', verbose_name='Çalışan')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members', verbose_name='Grup')
    role_in_group = models.CharField('Gruptaki Rol', max_length=32, choices=ROLE_CHOICES, default='Üye')
    can_create_report = models.BooleanField(
        'Rapor Oluşturma Yetkisi',
        default=False,
        help_text="Bu kullanıcı rapor oluşturabilir."
    )
    added_at = models.DateTimeField('Gruba Ekleme Tarihi', auto_now_add=True)

    def __str__(self):
        return f"{self.member.list_name()} - {self.group.name}"

    def save(self, *args, **kwargs):
        # Role göre `can_create_report` otomatik ayarlanır
        self.can_create_report = self.role_in_group in ['Yönetici', 'Raportör']
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Grup Üyesi'  # Tekil isim
        verbose_name_plural = 'Grup Üyeleri'  # Çoğul isim

#group end

# Signals for base and inherited user models.

def svc_signal(instance):
    if hasattr(instance, 'user'):
        instance.first_name = instance.user.first_name
        instance.last_name = instance.user.last_name

@receiver(pre_save, sender=Employee)
def employee_callback(sender, instance, *args, **kwargs):
    svc_signal(instance)

def usr_signal(instance, svc_member, svc_callback):
    pre_save.disconnect(svc_callback)
    svc_member.first_name = instance.first_name
    svc_member.last_name = instance.last_name
    svc_member.save()
    pre_save.connect(svc_callback)

@receiver(pre_save, sender=User)
def user_callback(sender, instance, *args, **kwargs):
    if hasattr(instance, 'employee'):
        usr_signal(instance, instance.employee, employee_callback)





# From Meetings Folder:

from django.db import models
from django.contrib.auth.models import User
from entity.models import Unit, Employee, Group, MemberGroup
from datetime import datetime


class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    meeting_name = models.CharField('Toplantı Adı', max_length=32, blank=False, null=False)
    date = models.DateTimeField('Toplantı Tarihi', default=datetime.now)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='created_meetings') #takım üyesi oalrak değiştirmiştim, ama sadece isim tutuyor diye geri aldımi rektörlük vb başka gruplar için meeting açabilsin
    parent_meeting = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    meeting_file = models.FileField('Toplantı Dosyası', upload_to='meeting_files/', null=True, blank=True)  # Yeni alan

    def __str__(self):
        return self.meeting_name

    class Meta:
        verbose_name = 'Toplantı'  # Tekil isim
        verbose_name_plural = 'Toplantılar'  # Çoğul isim


class Attendants(models.Model):
    id = models.AutoField(primary_key=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendants')  # Katılımcının ait olduğu toplantı
    member = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attended_meetings')  # Katılımcı

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name} - {self.meeting.meeting_name}"

    class Meta:
        verbose_name = 'Toplantı Katılmcısı'  # Tekil isim
        verbose_name_plural = 'Toplantı Katılımcıları'  # Çoğul isim


class Topics(models.Model):
    id = models.AutoField(primary_key=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='topics')  # Maddenin ait olduğu toplantı
    topic_text = models.TextField('Gündem Maddesi', blank=False, null=False, default="Varsayılan gündem metni")

    def __str__(self):
        return f"Topic in Meeting {self.meeting.meeting_name}"

    class Meta:
        verbose_name = 'Toplantının Gündem Maddesi'  # Tekil isim
        verbose_name_plural = 'Toplantının Gündem Maddeleri'  # Çoğul isim


class Decisions(models.Model):
    DECISION_STATUS_CHOICES = [
        ('finalized', 'Karar Kesinleşti'),
        ('pending', 'Karar Kesinleşmedi'),
        ('cancelled', 'Karar İptal Edildi'),
        ('completed_later', 'Sonradan Tamamlandı'),
        ('cancelled_later', 'Sonradan İptal Edildi')
    ]

    id = models.AutoField(primary_key=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='decisions')  # Kararın ait olduğu toplantı
    responsible = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsible_decisions')  # Karardan sorumlu kişi
    decision_status = models.TextField('Durum', choices=DECISION_STATUS_CHOICES, default='pending')  # Karar durumu
    topic_group = models.CharField('Konu Grubu', max_length=64, blank=False, null=False)  # Konu grubu
    decision_text = models.TextField('Karar Metni', blank=False, null=False, default="Varsayılan karar metni")
    meeting_topic = models.ForeignKey(Topics, null=True, blank=True, on_delete=models.CASCADE, related_name='decisions')  # Kararın bağlı olduğu gündem maddesi
    decision_taken_date = models.DateTimeField('Kararın Alınma Tarihi', default=datetime.now)
    decision_finished_date = models.DateTimeField('Kararın Tamamlanma Tarihi', null=True, blank=True)
    decision_finish_text = models.TextField('Kararın Tamamlanma Yazısı', blank=True, null=True)
    evidence_file = models.FileField('Kanıt Dosyası', upload_to='decision_evidence/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Karar tamamlandı veya iptal edildiyse, tamamlanma tarihi alınma tarihi ile aynı olur
        if self.decision_status in ['finalized', 'cancelled']:
            self.decision_finished_date = self.decision_taken_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Decision in {self.meeting.meeting_name} - Status: {self.decision_status}"

    class Meta:
        verbose_name = 'Karar'  # Tekil isim
        verbose_name_plural = 'Kararlar'  # Çoğul isim




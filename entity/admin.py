# Merged File: admin.py

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.forms import TextInput
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ExportMixin

from .models import Member, Employee, Unit, Group, MemberGroup

# All admin registration classes in the application

class NewUserResource(resources.ModelResource):
    class Meta:
        model = User

class NewUserAdmin(UserAdmin, ImportExportModelAdmin):
    resource_class = NewUserResource
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff',]
    list_filter = ['is_active',]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['username',]

        else:
            return []

admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)

class MemberResource(resources.ModelResource):
    class Meta:
        model = Member

class MemberAdmin(ImportExportModelAdmin):
    resource_class = MemberResource
    list_display = ['list_name', 'phone_country', 'phone_part2', 'phone_part3', 'phone_part4', 'user', 'role', 'is_active', 'can_create_group', 'title']
    list_display_links = ['list_name']
    list_filter = ['role']  # `can_create_report` kaldırıldı
    search_fields = ['last_name', 'first_name', 'user__username']
    raw_id_fields = ['user']
    formfield_overrides = {models.CharField: {'widget': TextInput(attrs={'size': '32'})}}

    def get_fieldsets(self, request, obj=None):
        if obj:
            return [
                ('Details', {
                    'fields': [('long_name'), ('phone_country', 'phone_part2', 'phone_part3', 'phone_part4'), ('user'), ('title')]
                }),
                ('Status', {
                    'fields': [('role', 'is_active', 'can_create_group')]  # `can_create_report` kaldırıldı
                }),
            ]
        else:
            return [
                ('Details', {
                    'fields': [('phone_country', 'phone_part2', 'phone_part3', 'phone_part4'), ('user')]
                }),
                ('Status', {
                    'fields': [('role', 'is_active', 'can_create_group')]  # `can_create_report` kaldırıldı
                }),
            ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['long_name', 'user', 'is_active']
        else:
            return ['long_name', 'is_active']


class EmployeeResource(MemberResource):
    class Meta:
        model = Employee

class EmployeeAdmin(MemberAdmin):
    resource_class = EmployeeResource
    # `unit` alanını listede göstermek için
    list_display = MemberAdmin.list_display + ['unit']
    list_display = [field for field in list_display if field != 'can_create_report']  # `can_create_report` kaldırıldı

    # `unit` alanını düzenlenebilir form alanlarına eklemek için
    def get_fieldsets(self, request, obj=None):
        if obj:
            return [('Details', {'fields': [('long_name'), ('phone_country', 'phone_part2', 'phone_part3', 'phone_part4'), ('user', 'unit'), ('title')]}),
                    ('Status', {'fields': [('role', 'is_active', 'can_create_group')]})]
        else:
            return [('Details', {'fields': [('phone_country', 'phone_part2', 'phone_part3', 'phone_part4'), ('user', 'unit')]}),
                    ('Status', {'fields': [('role', 'is_active', 'can_create_group')]})]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['long_name', 'user', 'is_active']
        else:
            return ['long_name', 'is_active']


admin.site.register(Employee, EmployeeAdmin)


class UnitResource(resources.ModelResource):
    class Meta:
        model = Unit

class UnitAdmin(ImportExportModelAdmin):
    resource_class = UnitResource
    list_display = ['parent_unit', 'name']
    list_display_links = ['name',]
    list_filter = []
    search_fields = ['name']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        }

    def get_fieldsets(self, request, obj=None):
        if obj:
            return [('Birim Bilgileri', {'fields':[('parent_unit', 'name')]})]
        else:
            return [('Birim Bilgileri', {'fields':[('parent_unit', 'name')]})]

    def get_readonly_fields(self, request, obj=None):
        return ['id']

admin.site.register(Unit, UnitAdmin)


#gruplar

class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_at', 'member_count']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Üye Sayısı'


class MemberGroupResource(resources.ModelResource):
    class Meta:
        model = MemberGroup


class MemberGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'member', 'group', 'role_in_group', 'can_create_report', 'added_at']
    list_filter = ['group', 'role_in_group', 'can_create_report']
    search_fields = ['member__first_name', 'member__last_name', 'group__name']

    def get_readonly_fields(self, request, obj=None):
        return ['can_create_report']



admin.site.register(Group, GroupAdmin)
admin.site.register(MemberGroup, MemberGroupAdmin)

#gruplar son



# From Meetings Folder:

from django.contrib import admin
from .models import Meeting, Attendants, Decisions

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('meeting_name', 'date', 'created_by')  # 'get_group_name' kaldırıldı
    list_filter = ('date',)  # 'group' kaldırıldı
    search_fields = ('meeting_name', 'created_by__first_name', 'created_by__last_name')
    ordering = ('-date',)


@admin.register(Attendants)
class AttendantsAdmin(admin.ModelAdmin):
    list_display = ('get_meeting_name', 'get_member_name')
    list_filter = ('meeting__date',)  # 'meeting__group' kaldırıldı
    search_fields = ('meeting__meeting_name', 'member__first_name', 'member__last_name')

    def get_meeting_name(self, obj):
        return obj.meeting.meeting_name
    get_meeting_name.short_description = "Toplantı Adı"

    def get_member_name(self, obj):
        return f"{obj.member.first_name} {obj.member.last_name}"
    get_member_name.short_description = "Katılımcı Adı"


@admin.register(Decisions)
class DecisionsAdmin(admin.ModelAdmin):
    list_display = ('get_meeting_name', 'get_responsible_name', 'decision_status', 'topic_group')
    list_filter = ('decision_status',)  # 'meeting__group' kaldırıldı
    search_fields = ('meeting__meeting_name', 'responsible__first_name', 'responsible__last_name', 'topic_group')

    def get_meeting_name(self, obj):
        return obj.meeting.meeting_name
    get_meeting_name.short_description = "Toplantı Adı"

    def get_responsible_name(self, obj):
        if obj.responsible:
            return f"{obj.responsible.first_name} {obj.responsible.last_name}"
        return "Belirtilmemiş"
    get_responsible_name.short_description = "Sorumlu Adı"
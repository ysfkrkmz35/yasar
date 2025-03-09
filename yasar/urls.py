"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from . import authentication
from . import employee
from entity.views import unit_hierarchy,create_group,view_groups,index
from entity.views import (upload_meeting_file,update_decision,create_meeting,add_attendant,add_decision, add_attendants_decisions,
                            delete_decision,delete_attendant,generate_meeting_pdf,view_decisions,view_meetings,cancel_meeting,get_group_members,
                            add_group_to_meeting,add_topic_to_meeting,delete_topic)


urlpatterns = [
    #re_path(r'^$', TemplateView.as_view(template_name='yasar/index.html'), name='index'),
    re_path(r'^$', index, name='index'),
    re_path(r'^login/$', authentication.LoginView.as_view(template_name='yasar/login.html'), name='login'),
    re_path(r'^logout/$', authentication.logout_view, name='logout'),
    re_path(r'^quality/quality_index/$', TemplateView.as_view(template_name='quality/quality_index.html'), name='quality_index'),
    re_path(r'^yasar/employee_index/$', employee.index, name='employee_index'),
    re_path(r'^yasar/employee_manage/$', employee.manage, name='employee_manage'),
#    re_path(r'^service/order_report/$', order.report, name='order_report'),
    path("admin/", admin.site.urls),

    #unit hierarchy için url
    path('units/', unit_hierarchy, name='unit_hierarchy'),
    path('units/<int:unit_id>/', unit_hierarchy, name='unit_hierarchy_detail'),

    #unit hierarchy içindeki toplantılar için url
    path('user/meetings/', view_meetings, name='view_meetings'),

    path('create/', create_meeting, name='create_meeting'),

    #----------------add_attendant_decisions.html url'leri------------------
    # Katılımcı ve Grup İşlemleri
    path('<int:meeting_id>/add-attendant/', add_attendant, name='add_attendant'),
    path('<int:meeting_id>/add-group-to-meeting/', add_group_to_meeting, name='add_group_to_meeting'),  # Grup ekleme
    path('delete-attendant/<int:attendant_id>/', delete_attendant, name='delete_attendant'),

    # Karar İşlemleri
    path('<int:meeting_id>/add-decision/', add_decision, name='add_decision'),
    path('delete-decision/<int:decision_id>/', delete_decision, name='delete_decision'),

    # Gündem Maddesi İşlemleri
    path('<int:meeting_id>/add-topic-to-meeting/', add_topic_to_meeting, name='add_topic_to_meeting'),
    path('delete-topic/<int:topic_id>/', delete_topic, name='delete_topic'),

    # Genel Toplantı İşlemleri
    path('<int:meeting_id>/add-attendants-decisions/', add_attendants_decisions, name='add_attendants_decisions'),
    path('<int:meeting_id>/upload-meeting-file/', upload_meeting_file, name='upload_meeting_file'),
    path('<int:meeting_id>/cancel-meeting/', cancel_meeting, name='cancel_meeting'),

    # Grup Üyesi Al
    path('get-group-members/', get_group_members, name='get_group_members'),


    #pdf indirme tuşu url
    path('<int:meeting_id>/download_pdf/', generate_meeting_pdf, name='download_meeting_pdf'),

    # meetings/urls.py
    path('<int:meeting_id>/upload_file/', upload_meeting_file, name='upload_meeting_file'),


    path('decisions/', view_decisions, name='view_decisions'),
    path('decisions/<int:decision_id>/update/', update_decision, name='update_decision'),

    path('create_group/', create_group, name='create_group'),
    path('view_groups/', view_groups, name='view_groups'),

    #pdf pop-up için
    path('generate-meeting-pdf/<int:meeting_id>/', generate_meeting_pdf, name='generate_meeting_pdf'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



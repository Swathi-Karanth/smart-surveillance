from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.login_user, name='login'),
    path('login', views.login_user, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('e_contact/', views.e_contact, name='e_contact'),
    path('roles_list/', views.roles_list, name='roles_list'),
    path('add_contacts/', views.add_contacts, name='add_contacts'),
    path('update_contacts/<int:pk>', views.update_contacts, name='update_contacts'),
    path('staff/', views.staff, name='staff'),
    path('update_staff/<int:pk>', views.update_staff, name='update_staff'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('add_role/', views.add_role, name='add_role'),
    path('visitor_ledger/', views.visitor, name='visitor'),
    path('add_visitor/', views.add_visitor, name='add_visitor'),
    path('incidents/', views.incident, name='incident'),
    path('add_incidents/', views.add_incidents, name='add_incidents'),
    path('update_incidents/', views.update_incidents, name='update_incidents'),
    path('delete_staff/<int:pk>', views.delete_staff, name='delete_staff'),
    path('delete_visitor/<int:pk>', views.delete_visitor, name='delete_visitor'),
    path('cctv_page/', views.cctv_page, name='Cctv'),
    path('play_video/', views.play_video, name='play_video'),
    path('error_404/', views.error_404, name='error_404'),
    path('update_visitor/<int:pk>', views.update_visitor, name='update_visitor'),
    path('profile/<int:pk>', views.profile, name='profile'),
]


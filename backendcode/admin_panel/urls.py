from django.urls import path
from .views import (
    AdminDashboardView,
    AdminUserListView, AdminUserDetailView, AdminUserToggleActiveView,
    AdminDoctorListView, AdminDoctorDetailView, AdminDoctorToggleActiveView,
    AdminSpecialtyListView,
    AdminPatientListView, AdminPatientDetailView,
    AdminAppointmentListView, AdminAppointmentDetailView, AdminAppointmentStatusView,
    AdminNotificationListView,
    SecDashboardView, SecAppointmentListView,
    SecAppointmentConfirmView, SecAppointmentCancelView, SecAppointmentCreateView,
    SecPatientListView, SecDoctorListView, SecProfileView,
)

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('users/',                        AdminUserListView.as_view(),         name='admin_user_list'),
    path('users/<int:user_id>/',          AdminUserDetailView.as_view(),       name='admin_user_detail'),
    path('users/<int:user_id>/toggle-active/', AdminUserToggleActiveView.as_view(), name='admin_user_toggle'),
    path('doctors/',                           AdminDoctorListView.as_view(),         name='admin_doctor_list'),
    path('doctors/<int:doctor_id>/',           AdminDoctorDetailView.as_view(),       name='admin_doctor_detail'),
    path('doctors/<int:doctor_id>/toggle-active/', AdminDoctorToggleActiveView.as_view(), name='admin_doctor_toggle'),
    path('specialties/', AdminSpecialtyListView.as_view(), name='admin_specialty_list'),
    path('patients/',                    AdminPatientListView.as_view(),   name='admin_patient_list'),
    path('patients/<int:patient_id>/',   AdminPatientDetailView.as_view(), name='admin_patient_detail'),
    path('appointments/',                          AdminAppointmentListView.as_view(),   name='admin_appointment_list'),
    path('appointments/<int:appointment_id>/',     AdminAppointmentDetailView.as_view(), name='admin_appointment_detail'),
    path('appointments/<int:appointment_id>/status/', AdminAppointmentStatusView.as_view(), name='admin_appointment_status'),
    path('notifications/', AdminNotificationListView.as_view(), name='admin_notification_list'),

    # Secretary Panel API
    path('sec/dashboard/',                     SecDashboardView.as_view(),            name='sec_dashboard'),
    path('sec/appointments/',                  SecAppointmentListView.as_view(),       name='sec_appointment_list'),
    path('sec/appointments/<int:appointment_id>/confirm/', SecAppointmentConfirmView.as_view(), name='sec_appointment_confirm'),
    path('sec/appointments/<int:appointment_id>/cancel/',  SecAppointmentCancelView.as_view(),  name='sec_appointment_cancel'),
    path('sec/appointments/create/',           SecAppointmentCreateView.as_view(),     name='sec_appointment_create'),
    path('sec/patients/',                      SecPatientListView.as_view(),           name='sec_patient_list'),
    path('sec/doctors/',                       SecDoctorListView.as_view(),            name='sec_doctor_list'),
    path('sec/profile/',                       SecProfileView.as_view(),               name='sec_profile'),
]

from django.urls import path
from .views import (
    PatientDashboardView,
    PatientProfileView,
    MyAppointmentsView,
    BookAppointmentView,
    DoctorAvailabilityView,
    ConfirmBookAppointmentView,
    CancelPatientAppointmentView,
    ReschedulePatientAppointmentView,
)

urlpatterns = [
    path('dashboard/',                                    PatientDashboardView.as_view(),           name='patient_dashboard'),
    path('profile/',                                      PatientProfileView.as_view(),              name='patient_profile'),
    path('appointments/',                                 MyAppointmentsView.as_view(),              name='my_appointments'),
    path('appointments/<int:appointment_id>/cancel/',     CancelPatientAppointmentView.as_view(),    name='patient_cancel_appointment'),
    path('appointments/<int:appointment_id>/reschedule/',  ReschedulePatientAppointmentView.as_view(), name='patient_reschedule_appointment'),
    path('book/',                                         BookAppointmentView.as_view(),             name='book_appointment'),
    path('book/doctor-availability/<int:doctor_id>/',     DoctorAvailabilityView.as_view(),          name='doctor_availability'),
    path('book/confirm/<int:doctor_id>/',                 ConfirmBookAppointmentView.as_view(),      name='confirm_book'),
]
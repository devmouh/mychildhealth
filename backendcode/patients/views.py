from datetime import datetime

from django.utils.timezone import now
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from consultations.models import Appointment
from users.models import Doctors, Specialty, Patients
from users.permissions import IsParent
from notifications.utils import create_notification


# ─── Dashboard ────────────────────────────────────────────────────────────────

class PatientDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsParent]

    def get(self, request):
        children = Patients.objects.filter(parent=request.user)
        data = [
            {
                'id':                    c.id,
                'first_name':            c.first_name,
                'last_name':             c.last_name,
                'birth_date':            c.birth_date,
                'gender':                c.gender,
                'groupe_sanguin':        c.groupe_sanguin,
                'date_creation_dossier': c.date_creation_dossier,
                'photo_url':             request.build_absolute_uri(c.photo.url) if c.photo else None,
            }
            for c in children
        ]
        return Response({'children': data})


# ─── Profile ──────────────────────────────────────────────────────────────────

class PatientProfileView(APIView):
    permission_classes = [IsAuthenticated, IsParent]

    def get(self, request):
        children = Patients.objects.filter(parent=request.user)
        data = [
            {
                'id':                    c.id,
                'first_name':            c.first_name,
                'last_name':             c.last_name,
                'birth_date':            c.birth_date,
                'gender':                c.gender,
                'groupe_sanguin':        c.groupe_sanguin,
                'telephone_parent':      c.telephone_parent,
                'email':                 c.email,
                'date_creation_dossier': c.date_creation_dossier,
                'photo_url':             request.build_absolute_uri(c.photo.url) if c.photo else None,
                'parent_phone':          request.user.phone,
                'parent_email':          request.user.email,
            }
            for c in children
        ]
        return Response({'children': data})


# ─── Appointments list ────────────────────────────────────────────────────────

class MyAppointmentsView(APIView):
    permission_classes = [IsAuthenticated, IsParent]

    def get(self, request):
        appointments = (
            Appointment.objects
            .filter(patient__parent=request.user)
            .select_related('doctor__user', 'patient')
            .order_by('-date_rdv')
        )

        status_filter = request.query_params.get('status', '').strip()
        date_filter   = request.query_params.get('date', '').strip()
        doctor_name   = request.query_params.get('doctor_name', '').strip()

        if status_filter and status_filter != 'All':
            appointments = appointments.filter(status=status_filter)
        if date_filter:
            appointments = appointments.filter(date_rdv__date=date_filter)
        if doctor_name:
            appointments = appointments.filter(doctor__user__last_name__icontains=doctor_name)

        data = [
            {
                'id':           a.id,
                'patient':      f"{a.patient.first_name} {a.patient.last_name}",
                'patient_id':   a.patient.id,
                'doctor':       f"Dr. {a.doctor.user.last_name} {a.doctor.user.first_name}",
                'doctor_id':    a.doctor.id,
                'date_rdv':     a.date_rdv,
                'heure':        a.heure,
                'motif':        a.motif,
                'status':       a.status,
                'status_label': a.get_status_display(),
                'reason':       a.reason,
            }
            for a in appointments
        ]
        return Response({
            'appointments':   data,
            'status_choices': Appointment.STATUS_CHOICES,
        })


# ─── Doctor availability — time slots ──────────────────────────────────────

class DoctorAvailabilityView(APIView):
    permission_classes = [IsAuthenticated, IsParent]

    def get(self, request, doctor_id):
        doctor = get_object_or_404(Doctors, id=doctor_id, actif=True)

        date_str = str(request.query_params.get('date', '')).strip()
        if not date_str:
            date_str = str(now().date())

        # Parse horaire_travail to get start/end hours
        work_hours = doctor.horaire_travail.strip() if doctor.horaire_travail else '9:00-15:00'
        try:
            import re
            times = re.findall(r'\d{1,2}:\d{2}', work_hours)
            if len(times) >= 2:
                start_h = int(times[0].split(':')[0])
                end_h = int(times[1].split(':')[0])
            else:
                start_h, end_h = 9, 15
        except (ValueError, IndexError):
            start_h, end_h = 9, 15

        # Generate hourly slots
        all_slots = []
        for h in range(start_h, end_h):
            label = f"{h}:00-{h+1}:00"
            all_slots.append(label)

        # Fetch existing appointments for this doctor on this date
        existing = Appointment.objects.filter(
            doctor=doctor,
            date_rdv__date=date_str,
        ).exclude(status='CANCELLED')

        booked_times = set()
        for a in existing:
            t = a.date_rdv.time()
            booked_times.add(f"{t.hour}:00-{t.hour+1}:00")

        slots = []
        for slot in all_slots:
            slots.append({
                'time': slot,
                'is_available': slot not in booked_times,
            })

        return Response({
            'doctor_id': doctor_id,
            'date': date_str,
            'horaire_travail': work_hours,
            'slots': slots,
        })

class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated, IsParent]

    def get(self, request):
        doctors      = Doctors.objects.select_related('user', 'specialty').filter(actif=True)
        specialities = Specialty.objects.all()

        speciality  = request.query_params.get('speciality', '').strip()
        city        = request.query_params.get('city', '').strip()
        doctor_name = request.query_params.get('doctor_name', '').strip()

        if speciality and speciality != 'All':
            doctors = doctors.filter(specialty__name=speciality)
        if doctor_name:
            doctors = doctors.filter(user__last_name__icontains=doctor_name)
        if city:
            doctors = doctors.filter(ville__icontains=city)

        children = Patients.objects.filter(parent=request.user)

        return Response({
            'doctors': [
                {
                    'id':              d.id,
                    'first_name':      d.user.first_name,
                    'last_name':       d.user.last_name,
                    'specialty':       d.specialty.name if d.specialty else '',
                    'bio':             d.bio,
                    'ville':           d.ville,
                    'horaire_travail': d.horaire_travail,
                    'photo':           request.build_absolute_uri(d.photo.url) if d.photo else None,
                }
                for d in doctors
            ],
            'specialities': [{'id': s.id, 'name': s.name} for s in specialities],
            'children': [
                {'id': c.id, 'first_name': c.first_name, 'last_name': c.last_name}
                for c in children
            ],
        })


# ─── Confirm / create appointment ────────────────────────────────────────────

class ConfirmBookAppointmentView(APIView):
    permission_classes = [IsAuthenticated, IsParent]

    def post(self, request, doctor_id):
        doctor = get_object_or_404(Doctors, id=doctor_id, actif=True)

        child_id    = str(request.data.get('child_id',    '')).strip()
        date_value  = str(request.data.get('date',        '')).strip()
        time_value  = str(request.data.get('time',        '')).strip()
        summary     = str(request.data.get('summary',     '')).strip()
        description = str(request.data.get('description', '')).strip()

        if not all([child_id, date_value, time_value]):
            return Response(
                {'detail': 'Veuillez remplir tous les champs obligatoires.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        child = get_object_or_404(Patients, id=child_id, parent=request.user)

        if date_value < str(now().date()):
            return Response(
                {'detail': 'Impossible de réserver une date passée.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Appointment.objects.filter(
            doctor=doctor,
            date_rdv__date=date_value,
            date_rdv__time=time_value,
        ).exists():
            return Response(
                {'detail': 'Ce créneau est déjà pris. Veuillez en choisir un autre.'},
                status=status.HTTP_409_CONFLICT
            )

        date_rdv = datetime.strptime(f"{date_value} {time_value}", "%Y-%m-%d %H:%M")
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=child,
            date_rdv=date_rdv,
            motif=summary,
            reason=f"{summary}\n{description}".strip(),
            status='PENDING',
            created_by=request.user,
        )

        # ── Notify the doctor about the new appointment ───────────────────────
        create_notification(
            user=doctor.user,
            type_notif='RDV',
            contenu=f"Nouveau rendez-vous de {child.first_name} {child.last_name} le {date_value} à {time_value}."
        )

        return Response(
            {'detail': 'Rendez-vous réservé avec succès.', 'appointment_id': appointment.id},
            status=status.HTTP_201_CREATED
        )


class CancelPatientAppointmentView(APIView):
    permission_classes = [IsAuthenticated, IsParent]

    def patch(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id, patient__parent=request.user)
        if appointment.status in ('COMPLETED', 'CANCELLED'):
            return Response(
                {'detail': 'Impossible d\'annuler ce rendez-vous.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        appointment.status = 'CANCELLED'
        appointment.save()
        return Response({'detail': 'Rendez-vous annulé avec succès.'})


class ReschedulePatientAppointmentView(APIView):
    permission_classes = [IsAuthenticated, IsParent]

    def patch(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id, patient__parent=request.user)
        if appointment.status in ('COMPLETED', 'CANCELLED'):
            return Response(
                {'detail': 'Impossible de modifier ce rendez-vous.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        date_value = str(request.data.get('date', '')).strip()
        time_value = str(request.data.get('time', '')).strip()

        if not date_value or not time_value:
            return Response(
                {'detail': 'Veuillez fournir une date et une heure.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if date_value < str(now().date()):
            return Response(
                {'detail': 'Impossible de réserver une date passée.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from datetime import datetime
        new_date = datetime.strptime(f"{date_value} {time_value}", "%Y-%m-%d %H:%M")
        appointment.date_rdv = new_date
        appointment.status = 'PENDING'
        appointment.save()
        return Response({'detail': 'Rendez-vous reprogrammé avec succès.', 'new_date': date_value, 'new_time': time_value})
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import update_session_auth_hash

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from consultations.models import Appointment, Consultation, Diagnostic, Traitement
from users.models import Patients, Specialty, Doctors, TraceAction
from users.permissions import IsDoctor
from notifications.utils import create_notification


def _get_doctor(user):
    try:
        return user.doctors
    except Doctors.DoesNotExist:
        raise PermissionDenied


def _log(user, action, table=""):
    TraceAction.objects.create(user=user, action=action, table_concernee=table)


# ─── Dashboard ────────────────────────────────────────────────────────────────

class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        doctor  = _get_doctor(request.user)
        base_qs = Appointment.objects.filter(doctor=doctor)
        return Response({
            'total_appointments': base_qs.count(),
            'pending':   base_qs.filter(status='PENDING').count(),
            'confirmed': base_qs.filter(status='CONFIRMED').count(),
            'completed': base_qs.filter(status='COMPLETED').count(),
            'cancelled': base_qs.filter(status='CANCELLED').count(),
        })


# ─── Profile ──────────────────────────────────────────────────────────────────

class DoctorProfileView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    parser_classes     = [MultiPartParser, FormParser]

    def get(self, request):
        user         = request.user
        doctor       = _get_doctor(user)
        specialities = Specialty.objects.all()
        return Response({
            'first_name':      user.first_name,
            'last_name':       user.last_name,
            'phone':           getattr(user, 'phone', ''),
            'email':           user.email,
            'bio':             doctor.bio,
            'ville':           doctor.ville,
            'horaire_travail': doctor.horaire_travail,
            'actif':           doctor.actif,
            'photo':           request.build_absolute_uri(doctor.photo.url) if doctor.photo else None,
            'specialty':       {'id': doctor.specialty.id, 'name': doctor.specialty.name} if doctor.specialty else None,
            'address': {
                'address_line': getattr(user.address, 'address_line', ''),
                'region':       getattr(user.address, 'region', ''),
                'city':         getattr(user.address, 'city', ''),
                'code_postal':  getattr(user.address, 'code_postal', ''),
            } if getattr(user, 'address', None) else {},
            'specialities': [{'id': s.id, 'name': s.name} for s in specialities],
        })

    def patch(self, request):
        user   = request.user
        doctor = _get_doctor(user)
        data   = request.data

        user.first_name = data.get('first_name', user.first_name).strip()
        user.last_name  = data.get('last_name',  user.last_name).strip()
        user.phone      = data.get('phone', getattr(user, 'phone', '')).strip()

        if getattr(user, 'address', None):
            user.address.address_line = data.get('address_line', user.address.address_line).strip()
            user.address.region       = data.get('region',       user.address.region).strip()
            user.address.city         = data.get('city',         user.address.city).strip()
            user.address.code_postal  = data.get('code_postal',  user.address.code_postal).strip()
            user.address.save()

        spec_id = str(data.get('speciality', '')).strip()
        if spec_id:
            get_object_or_404(Specialty, id=spec_id)
            doctor.specialty_id = spec_id

        doctor.bio             = data.get('bio',             doctor.bio).strip()
        doctor.ville           = data.get('ville',           doctor.ville).strip()
        doctor.horaire_travail = data.get('horaire_travail', doctor.horaire_travail).strip()

        if 'photo' in request.FILES:
            doctor.photo = request.FILES['photo']

        user.save()
        doctor.save()
        _log(user, 'UPDATE_PROFILE', 'Doctors')
        return Response({'detail': 'Profil mis à jour avec succès.'})


# ─── Appointments ─────────────────────────────────────────────────────────────

class DoctorAppointmentsView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        doctor        = _get_doctor(request.user)
        status_filter = request.query_params.get('status', '').strip()
        appointments  = (
            Appointment.objects
            .filter(doctor=doctor)
            .select_related('patient', 'doctor__user')
            .order_by('-date_rdv')
        )
        if status_filter and status_filter != 'All':
            appointments = appointments.filter(status=status_filter)

        data = [
            {
                'id':           a.id,
                'patient_id':   a.patient.id,
                'patient':      f"{a.patient.first_name} {a.patient.last_name}",
                'date_rdv':     a.date_rdv,
                'heure':        a.heure,
                'motif':        a.motif,
                'status':       a.status,
                'status_label': a.get_status_display(),
                'reason':       a.reason,
            }
            for a in appointments
        ]
        return Response({'appointments': data, 'status_choices': Appointment.STATUS_CHOICES})

    def patch(self, request):
        doctor     = _get_doctor(request.user)
        app_id     = str(request.data.get('appointment_id', '')).strip()
        new_status = str(request.data.get('status', '')).strip()

        appointment = get_object_or_404(Appointment, id=app_id, doctor=doctor)

        valid_statuses = dict(Appointment.STATUS_CHOICES).keys()
        if new_status not in valid_statuses:
            return Response({'detail': 'Statut invalide.'}, status=status.HTTP_400_BAD_REQUEST)
        if appointment.status == 'COMPLETED':
            return Response({'detail': 'Impossible de modifier une consultation terminée.'}, status=status.HTTP_400_BAD_REQUEST)

        appointment.status = new_status
        appointment.save()
        _log(request.user, f'UPDATE_APPOINTMENT_STATUS:{new_status}', 'Appointment')

        # ── Notify the parent about the status change ─────────────────────────
        status_labels = {'CONFIRMED': 'confirmé', 'CANCELLED': 'annulé', 'COMPLETED': 'terminé'}
        if new_status in status_labels:
            create_notification(
                user=appointment.patient.parent,
                type_notif='RDV',
                contenu=f"Votre rendez-vous du {appointment.date_rdv:%d/%m/%Y} a été {status_labels[new_status]}."
            )

        return Response({'detail': 'Statut mis à jour.'})


# ─── Consultations ────────────────────────────────────────────────────────────

class DoctorConsultationsView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        doctor = _get_doctor(request.user)
        consultations = (
            Consultation.objects
            .filter(appointment__doctor=doctor)
            .select_related('appointment__patient')
            .order_by('-date_consultation')
        )
        data = [
            {
                'id':                c.id,
                'patient':           f"{c.appointment.patient.first_name} {c.appointment.patient.last_name}",
                'date_consultation': c.date_consultation,
                'poids':             c.poids,
                'taille':            c.taille,
                'temperature':       c.temperature,
                'observation':       c.observation,
            }
            for c in consultations
        ]
        return Response({'consultations': data})


# ─── Diagnostics ──────────────────────────────────────────────────────────────

class DoctorDiagnosticsView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        doctor = _get_doctor(request.user)
        diagnostics = (
            Diagnostic.objects
            .filter(consultation__appointment__doctor=doctor)
            .select_related('consultation__appointment__patient')
            .order_by('-consultation__date_consultation')
        )
        data = [
            {
                'id':                  d.id,
                'patient':             f"{d.consultation.appointment.patient.first_name} {d.consultation.appointment.patient.last_name}",
                'nom_maladie':         d.nom_maladie,
                'type_maladie':        d.type_maladie,
                'type_label':          d.get_type_maladie_display(),
                'gravite':             d.gravite,
                'gravite_label':       d.get_gravite_display(),
                'commentaire_medical': d.commentaire_medical,
                'explication_parent':  d.explication_parent,
            }
            for d in diagnostics
        ]
        return Response({'diagnostics': data})


# ─── Treatments ───────────────────────────────────────────────────────────────

class DoctorTreatmentsView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        doctor = _get_doctor(request.user)
        treatments = (
            Traitement.objects
            .filter(consultation__appointment__doctor=doctor)
            .select_related('consultation__appointment__patient')
            .order_by('-consultation__date_consultation')
        )
        data = [
            {
                'id':           t.id,
                'patient':      f"{t.consultation.appointment.patient.first_name} {t.consultation.appointment.patient.last_name}",
                'medicament':   t.medicament,
                'dose':         t.dose,
                'duree':        t.duree,
                'instructions': t.instructions,
            }
            for t in treatments
        ]
        return Response({'treatments': data})


# ─── Doctor's Patient List ─────────────────────────────────────────────

class DoctorPatientsView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        doctor = _get_doctor(request.user)
        # Get all patients who have appointments with this doctor
        patient_ids = (
            Appointment.objects
            .filter(doctor=doctor)
            .values_list('patient_id', flat=True)
            .distinct()
        )
        patients = Patients.objects.filter(id__in=patient_ids)
        data = [
            {
                'id':                p.id,
                'first_name':        p.first_name,
                'last_name':         p.last_name,
                'name':              f"{p.first_name} {p.last_name}",
                'birth_date':        p.birth_date,
                'gender':            p.gender,
                'groupe_sanguin':    p.groupe_sanguin,
                'telephone_parent':  p.telephone_parent,
                'email':             p.email,
                'parent_name':       f"{p.parent.first_name} {p.parent.last_name}" if p.parent else '',
                'parent_relation':   'Mère' if p.parent and p.parent.gender == 'F' else 'Père',
                'allergies':         [],
                'medical_history':   [],
                'poids':             '',
                'taille':            '',
                'status':            'ACTIVE',
                'photo_url':         None,
            }
            for p in patients
        ]
        return Response({'patients': data})


# ─── Change Password (doctor) ──────────────────────────────────────────

class DoctorChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password', '')
        new_password = request.data.get('new_password', '')

        if not old_password or not new_password:
            return Response(
                {'detail': 'old_password et new_password sont requis.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.check_password(old_password):
            return Response(
                {'detail': 'Ancien mot de passe incorrect.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(new_password) < 8:
            return Response(
                {'detail': 'Le nouveau mot de passe doit contenir au moins 8 caractères.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        _log(user, 'CHANGE_PASSWORD', 'Users')
        return Response({'detail': 'Mot de passe changé avec succès.'})
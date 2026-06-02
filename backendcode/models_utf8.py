# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class ConsultationsAppointment(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_rdv = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey('UsersUsers', models.DO_NOTHING, blank=True, null=True)
    doctor = models.ForeignKey('UsersDoctors', models.DO_NOTHING)
    patient = models.ForeignKey('UsersPatients', models.DO_NOTHING)
    updated_at = models.DateTimeField()
    heure = models.TimeField(blank=True, null=True)
    motif = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'consultations_appointment'


class ConsultationsConsultation(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_consultation = models.DateTimeField()
    poids = models.DecimalField(max_digits=5, decimal_places=2)
    taille = models.DecimalField(max_digits=5, decimal_places=2)
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    observation = models.TextField()
    appointment = models.OneToOneField(ConsultationsAppointment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'consultations_consultation'


class ConsultationsDiagnostic(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom_maladie = models.CharField(max_length=200)
    type_maladie = models.CharField(max_length=20)
    gravite = models.CharField(max_length=20)
    commentaire_medical = models.TextField()
    consultation = models.ForeignKey(ConsultationsConsultation, models.DO_NOTHING)
    explication_parent = models.TextField()

    class Meta:
        managed = False
        db_table = 'consultations_diagnostic'


class ConsultationsTraitement(models.Model):
    id = models.BigAutoField(primary_key=True)
    medicament = models.CharField(max_length=200)
    dose = models.CharField(max_length=100)
    duree = models.CharField(max_length=100)
    instructions = models.TextField()
    consultation = models.ForeignKey(ConsultationsConsultation, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'consultations_traitement'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsersUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DocumentsDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom_fichier = models.CharField(max_length=255)
    type_doc = models.CharField(max_length=20)
    fichier = models.CharField(max_length=100, blank=True, null=True)
    date_upload = models.DateTimeField()
    consultation = models.ForeignKey(ConsultationsConsultation, models.DO_NOTHING, blank=True, null=True)
    patient = models.ForeignKey('UsersPatients', models.DO_NOTHING)
    uploaded_by = models.ForeignKey('UsersUsers', models.DO_NOTHING, blank=True, null=True)
    url_stockage = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'documents_document'


class MedicalAllergie(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=150)
    reaction = models.CharField(max_length=20)
    description = models.TextField()
    date_detection = models.DateField(blank=True, null=True)
    patient = models.ForeignKey('UsersPatients', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'medical_allergie'


class MedicalAntecedent(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField()
    type_antecedent = models.CharField(max_length=20)
    date_declaration = models.DateField(blank=True, null=True)
    patient = models.ForeignKey('UsersPatients', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'medical_antecedent'


class NotificationsMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    contenu = models.TextField()
    date_envoi = models.DateTimeField()
    lu = models.BooleanField()
    destinataire = models.ForeignKey('UsersUsers', models.DO_NOTHING)
    expediteur = models.ForeignKey('UsersUsers', models.DO_NOTHING, related_name='notificationsmessage_expediteur_set')

    class Meta:
        managed = False
        db_table = 'notifications_message'


class NotificationsNotification(models.Model):
    id = models.BigAutoField(primary_key=True)
    notif_type = models.CharField(max_length=20)
    title = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField()
    created_at = models.DateTimeField()
    appointment = models.ForeignKey(ConsultationsAppointment, models.DO_NOTHING, blank=True, null=True)
    recipient = models.ForeignKey('UsersUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'notifications_notification'


class TokenBlacklistBlacklistedtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey('UsersUsers', models.DO_NOTHING, blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'


class UsersAddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    address_line = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    code_postal = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'users_address'


class UsersDoctors(models.Model):
    id = models.BigAutoField(primary_key=True)
    bio = models.TextField()
    user = models.OneToOneField('UsersUsers', models.DO_NOTHING)
    specialty = models.ForeignKey('UsersSpecialty', models.DO_NOTHING)
    actif = models.BooleanField()
    horaire_travail = models.TextField()
    photo = models.CharField(max_length=100, blank=True, null=True)
    ville = models.CharField(max_length=100)
    numero_ordre_medecins = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'users_doctors'


class UsersPatients(models.Model):
    id = models.BigAutoField(primary_key=True)
    birth_date = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    last_name = models.CharField(max_length=50)
    parent = models.ForeignKey('UsersUsers', models.DO_NOTHING)
    groupe_sanguin = models.CharField(max_length=5)
    date_creation_dossier = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=254)
    telephone_parent = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'users_patients'


class UsersResteToken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('UsersUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_reste_token'


class UsersSecretaire(models.Model):
    id = models.BigAutoField(primary_key=True)
    bureau = models.CharField(max_length=100)
    telephone_interne = models.CharField(max_length=30)
    horaires_service = models.CharField(max_length=100)
    user = models.OneToOneField('UsersUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_secretaire'


class UsersSpecialty(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'users_specialty'


class UsersTraceaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    user = models.ForeignKey('UsersUsers', models.DO_NOTHING, blank=True, null=True)
    action = models.CharField(max_length=100)
    table_concernee = models.CharField(max_length=100)
    id_enregistrement = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_traceaction'


class UsersUsers(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)
    role = models.CharField(max_length=15)
    phone = models.CharField(max_length=20)
    address = models.ForeignKey(UsersAddress, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_users'


class UsersUsersGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    users = models.ForeignKey(UsersUsers, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_users_groups'
        unique_together = (('users', 'group'),)


class UsersUsersUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    users = models.ForeignKey(UsersUsers, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_users_user_permissions'
        unique_together = (('users', 'permission'),)

import os, re, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
import django
django.setup()
from django.conf import settings

DB_PATH = settings.DATABASES['default']['NAME']
SQL_PATH = os.path.join(os.path.dirname(__file__), '..', 'base de donnees', 'hospital_db_english_final.sql')

with open(SQL_PATH, 'r', encoding='utf-8') as f:
    sql = f.read()

# Remove ALTER SEQUENCE
sql = re.sub(r'^ALTER SEQUENCE.*;$', '', sql, flags=re.MULTILINE | re.IGNORECASE)

# Remove ::type casts
sql = re.sub(r'(\w+\.\w+)::date', r'date(\1)', sql)
sql = re.sub(r'(\w+)::date', r'date(\1)', sql)  # column without table prefix

# Handle NOW +/- INTERVAL
def replace_interval(m):
    inner = m.group(0)
    modifiers = []
    for match in re.finditer(r"[-+]\s*INTERVAL\s+'(\d+)\s*(day|days|hour|hours)'", inner, re.IGNORECASE):
        sign = match.group(0).strip()[0]
        num = match.group(1)
        unit = 'hours' if match.group(2) in ('hour', 'hours') else 'days'
        modifiers.append(f"'{sign}{num} {unit}'")
    if modifiers:
        return f"datetime('now', {', '.join(modifiers)})"
    return inner

sql = re.sub(
    r"NOW\s*\(\s*\)(?:\s*[-+]\s*INTERVAL\s+'[^']+'\s*(?:\s*[-+]\s*INTERVAL\s+'[^']+')*)",
    replace_interval, sql, flags=re.IGNORECASE
)
sql = sql.replace('NOW()', "datetime('now')")

# Fix secretaire INSERT (no photo column)
sql = sql.replace(
    "(user_id, bureau, telephone_interne, horaires_service, photo)",
    "(user_id, bureau, telephone_interne, horaires_service)"
)
sql = sql.replace(", ''\nFROM users_users u WHERE u.username = 'sec.fatima'", "\nFROM users_users u WHERE u.username = 'sec.fatima'")
sql = sql.replace(", ''\nFROM users_users u WHERE u.username = 'sec.karima'", "\nFROM users_users u WHERE u.username = 'sec.karima'")

# Import using Python's sqlite3 directly (not through Django cursor)
import sqlite3
conn = sqlite3.connect(DB_PATH)
conn.execute('PRAGMA journal_mode = OFF')
conn.execute('PRAGMA foreign_keys = OFF')

# Clear existing data
tables = ['notifications_notification','notifications_message','users_traceaction','documents_document','consultations_traitement','consultations_diagnostic','consultations_consultation','consultations_appointment','medical_antecedent','medical_allergie','users_patients','users_doctors','users_secretaire','users_users','users_specialty','users_address']
for t in tables:
    conn.execute(f'DELETE FROM {t}')

# Execute the SQL
print('Importing...')
statements = sql.split(';')
count = 0
for stmt in statements:
    lines = [l for l in stmt.split('\n') if not l.strip().startswith('--')]
    clean = '\n'.join(lines).strip()
    if not clean:
        continue
    try:
        conn.execute(clean)
        count += 1
    except Exception as e:
        print(f'Error ({count+1}): {e}')
        print(f'  SQL: {clean[:200]}')

conn.commit()
conn.execute('PRAGMA foreign_keys = ON')
conn.close()

# Fix passwords using Django
from users.models import Users
from django.contrib.auth.hashers import make_password
print(f'\nFixing passwords...')
hashed = make_password('12345678')
Users.objects.all().update(password=hashed, is_staff=True)
Users.objects.filter(role='ADMIN').update(is_superuser=True)

print('\n=== CREDENTIALS (all password: 12345678) ===')
for u in Users.objects.all().order_by('id'):
    print(f'  [{str(u.role or "UNKNOWN"):12}] {u.username}')

from users.models import Doctors, Patients
from consultations.models import Appointment, Consultation
print(f'\nUsers: {Users.objects.count()}, Doctors: {Doctors.objects.count()}, '
      f'Patients: {Patients.objects.count()}, Appointments: {Appointment.objects.count()}, '
      f'Consultations: {Consultation.objects.count()}')

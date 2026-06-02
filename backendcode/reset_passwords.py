import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()
from users.models import Users

for u in Users.objects.all():
    u.set_password('12345678')
    u.save()
    print(f"Password set: {u.username}")
print("Done!")

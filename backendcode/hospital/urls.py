import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def secretaire_panel(request):
    html_path = os.path.join(settings.BASE_DIR, 'secretaire_panel_fixed (1).html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    return HttpResponse(html, content_type='text/html; charset=utf-8')

urlpatterns = [
    path('admin/',             admin.site.urls),
    path('api/users/',         include('users.urls')),
    path('api/consultations/', include('consultations.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/messages/',      include('messaging.urls')),
    path('api/documents/',     include('documents.urls')),
    path('api/medical/',       include('medical_history.urls')),
    path('api/patient/',       include('patients.urls')),
    path('api/doctor/',        include('doctors.urls')),
    path('api/admin-panel/',   include('admin_panel.urls')),
    path('secretaire/',        secretaire_panel, name='secretaire_panel'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
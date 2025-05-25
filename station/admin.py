from django.contrib import admin
from .models import Station, Equipment, SensorData, DesalinationStation, Alert, StationParameters

# Enregistrements simples avec admin.site
admin.site.register(Station)
admin.site.register(Equipment)
admin.site.register(SensorData)

@admin.register(DesalinationStation)
class DesalinationStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'status')  # À adapter selon les champs réels
    search_fields = ('name', 'location')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('station', 'message', 'alert_type', 'timestamp')
    list_filter = ('alert_type', 'timestamp')
    search_fields = ('message',)

@admin.register(StationParameters)
class StationParametersAdmin(admin.ModelAdmin):
    list_display = ('station', 'parameter_name', 'value', 'timestamp')
    list_filter = ('parameter_name',)
    search_fields = ('parameter_name',)

# -----------------------------------------------
# Custom admin site
# -----------------------------------------------

from django.urls import path
from django.template.response import TemplateResponse

class CustomAdminSite(admin.AdminSite):
    site_header = 'ROMADES Dashboard'
    site_title = 'ROMADES Admin'
    index_title = 'Bienvenue dans le panneau de contrôle'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view))
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        context = dict(
            self.each_context(request),
            stations=DesalinationStation.objects.count(),
            alerts=Alert.objects.count(),
            params=StationParameters.objects.count()
        )
        return TemplateResponse(request, "admin/dashboard.html", context)

# Instancier le custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Enregistrer les modèles dans custom_admin_site (PAS dans admin.site ici)
custom_admin_site.register(DesalinationStation, DesalinationStationAdmin)
custom_admin_site.register(Alert, AlertAdmin)
custom_admin_site.register(StationParameters, StationParametersAdmin)

from django.utils.dateformat import DateFormat
from django.utils.timezone import localtime

def dashboard_view(request):
    stations = DesalinationStation.objects.count()
    alerts = Alert.objects.count()
    params = StationParameters.objects.order_by('timestamp')

    # Préparation des données pour Chart.js
    labels = [localtime(p.timestamp).strftime('%Y-%m-%d %H:%M') for p in params]
    values = [p.value for p in params]

    context = {
        'stations': stations,
        'alerts': alerts,
        'params': params,
        'labels': labels,
        'values': values,
    }
    return TemplateResponse(request, "admin/dashboard.html", context)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationViewSet, EquipmentViewSet, SensorViewSet, SensorDataViewSet
from . import views

# Définition du router avant l'utilisation
router = DefaultRouter()
router.register(r'stations', StationViewSet)
router.register(r'equipements', EquipmentViewSet)
router.register(r'sensors', SensorViewSet)
router.register(r'sensor-data', SensorDataViewSet)

urlpatterns = [
    path('add/', views.add_station, name='add_station'),
    path('list/', views.station_list, name='station_list'),
    path('stations/edit/<int:id>/', views.edit_station, name='edit_station'),
    path('stations/delete/<int:id>/', views.delete_station, name='delete_station'),

    # Routes pour gérer les équipements
    path('stations/<int:station_id>/equipments/', views.equipment_list, name='equipment_list'),
    path('stations/<int:station_id>/equipments/add/', views.add_equipment, name='add_equipment'),
    path('stations/<int:station_id>/equipments/edit/<int:equipment_id>/', views.edit_equipment, name='edit_equipment'),
    path('stations/<int:station_id>/equipments/delete/<int:equipment_id>/', views.delete_equipment, name='delete_equipment'),
    path('equipments/<int:equipment_id>/sensors/', views.sensor_data_view, name='sensor_data'),
    path('equipments/<int:equipment_id>/sensors/add/', views.add_sensor_data, name='add_sensor_data'),

    # Inclure les URLs du router
    path('', include(router.urls)),
    path('sensor-data-list/', views.sensor_data_list_view, name='sensor_data_list_view'),

     path('admin/dashboard/', views.dashboard_view, name='dashboard'),
   
   
]














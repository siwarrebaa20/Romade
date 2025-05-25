from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.utils.timezone import localtime

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from .models import (
    Station, Equipment, SensorData, Sensor,
    DesalinationStation, Alert, StationParameters
)
from .forms import StationForm, EquipmentForm, SensorDataForm
from .serializers import (
    StationSerializer, EquipmentSerializer,
    SensorSerializer, SensorDataSerializer
)

# Liste des stations
def station_list(request):
    stations = Station.objects.all()
    return render(request, 'station/station_list.html', {'stations': stations})

# Ajouter une station
def add_station(request):
    if request.method == "POST":
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Station ajoutée avec succès !')
            return redirect('station_list')
    else:
        form = StationForm()
    return render(request, 'station/add_station.html', {'form': form})

# Modifier une station
def edit_station(request, id):
    station = get_object_or_404(Station, id=id)
    if request.method == 'POST':
        form = StationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            return redirect('station_list')
    else:
        form = StationForm(instance=station)
    return render(request, 'station/edit_station.html', {'form': form, 'station': station})

# Supprimer une station
def delete_station(request, id):
    station = get_object_or_404(Station, id=id)
    if request.method == "POST":
        station.delete()
        return redirect('station_list')
    return render(request, 'station/delete_station.html', {'station': station})

# Vue des données capteurs
def sensor_data_view(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    sensor_data_list = SensorData.objects.filter(equipment=equipment)
    sensors = Sensor.objects.filter(equipment=equipment)
    return render(request, 'station/sensor_data.html', {
        'equipment': equipment,
        'sensor_data_list': sensor_data_list,
        'sensors': sensors
    })

# Ajouter une donnée capteur
def add_sensor_data(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    if request.method == 'POST':
        form = SensorDataForm(request.POST)
        if form.is_valid():
            sensor_data = form.save(commit=False)
            sensor_data.equipment = equipment
            sensor_data.save()
            return redirect('sensor_data', equipment_id=equipment.id)
    else:
        form = SensorDataForm()
    return render(request, 'station/add_sensor_data.html', {'form': form, 'equipment': equipment})

# Liste des équipements
def equipment_list(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    equipments = Equipment.objects.filter(station=station)
    return render(request, 'station/equipment_list.html', {'station': station, 'equipments': equipments})

# Ajouter un équipement
def add_equipment(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.station = station
            equipment.save()
            return redirect('equipment_list', station_id=station.id)
    else:
        form = EquipmentForm()
    return render(request, 'station/add_equipment.html', {'form': form, 'station': station})

# Modifier un équipement
def edit_equipment(request, station_id, equipment_id):
    station = get_object_or_404(Station, id=station_id)
    equipment = get_object_or_404(Equipment, id=equipment_id, station=station)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment_list', station_id=station.id)
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'station/edit_equipment.html', {'form': form, 'station': station, 'equipment': equipment})

# Supprimer un équipement
def delete_equipment(request, station_id, equipment_id):
    station = get_object_or_404(Station, id=station_id)
    equipment = get_object_or_404(Equipment, id=equipment_id, station=station)
    if request.method == 'POST':
        equipment.delete()
        return redirect('equipment_list', station_id=station.id)
    return render(request, 'station/delete_equipment.html', {'station': station, 'equipment': equipment})

# API ViewSets
class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

# Vue JSON des données capteurs
def sensor_data_list_view(request):
    sensor_data = SensorData.objects.select_related('equipment', 'sensor')
    serialized_data = SensorDataSerializer(sensor_data, many=True).data
    return render(request, 'station/sensor_data_list.html', {'sensor_data_list': serialized_data})

# Dashboard
def dashboard_view(request):
    stations = DesalinationStation.objects.count()
    alerts = Alert.objects.count()
    params = StationParameters.objects.order_by('timestamp')

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

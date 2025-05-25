from django import forms
from .models import Station,Equipment,SensorData
from django.core.exceptions import ValidationError
import datetime

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['nom', 'localisation', 'capacite', 'date_installation']

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if not nom:
            raise ValidationError('Le nom de la station ne peut pas être vide.')
        return nom

    def clean_localisation(self):
        localisation = self.cleaned_data.get('localisation')
        if not localisation:
            raise ValidationError('La localisation ne peut pas être vide.')
        return localisation

    def clean_capacite(self):
        capacite = self.cleaned_data.get('capacite')
        if capacite <= 0:
            raise ValidationError('La capacité doit être un nombre positif.')
        return capacite

    def clean_date_installation(self):
        date_installation = self.cleaned_data.get('date_installation')
        if date_installation and date_installation > datetime.date.today():
            raise ValidationError('La date d\'installation ne peut pas être dans le futur.')
        return date_installation
class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['nom', 'type', 'etat', 'station', 'date_installation']

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if not nom:
            raise ValidationError('Le nom de l\'équipement ne peut pas être vide.')
        return nom

    def clean_etat(self):
        etat = self.cleaned_data.get('etat')
        if not etat:
            raise ValidationError('L\'état de l\'équipement ne peut pas être vide.')
        return etat

    def clean_date_installation(self):
        date_installation = self.cleaned_data.get('date_installation')
        if date_installation and date_installation > datetime.date.today():
            raise ValidationError('La date d\'installation ne peut pas être dans le futur.')
        return date_installation
class SensorDataForm(forms.ModelForm):
    class Meta:
        model = SensorData
        fields = ['capteur', 'valeur']

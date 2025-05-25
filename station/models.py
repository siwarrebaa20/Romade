from django.db import models
from django.utils import timezone

# Station
class Station(models.Model):
    nom = models.CharField(max_length=200, default="Unknown")
    capacite = models.IntegerField(default=0)
    date_installation = models.DateField(default=timezone.now)
    localisation = models.CharField(max_length=200, default="Non spécifiée")

    def save(self, *args, **kwargs):
        self.nom = self.nom.strip().lower()
        self.localisation = self.localisation.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom.title()} | {self.capacite} m³ | {self.localisation.title()}"


# Equipement
class Equipment(models.Model):
    STATUS_CHOICES = [
        ('operational', 'Operational'),
        ('maintenance', 'Under Maintenance'),
        ('faulty', 'Faulty'),
        ('out_of_service', 'Out of Service'),
    ]

    ETAT_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    ]

    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=100)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='operational')
    etat = models.CharField(max_length=50, choices=ETAT_CHOICES, default='new')
    date_installation = models.DateField(default=timezone.now)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='equipements')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.get_statut_display()} | {self.get_etat_display()})"


# Capteur
class Sensor(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nom} ({self.type})"


# Données du capteur
class SensorData(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='sensor_data')  # Référence à l'équipement
    capteur = models.ForeignKey(Sensor, on_delete=models.CASCADE)  # Référence au capteur
    valeur = models.FloatField()  # Valeur mesurée par le capteur
    timestamp = models.DateTimeField(auto_now_add=True)  # Date et heure de la mesure

    def __str__(self):
        return f"{self.capteur.nom} - {self.valeur} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"

from django.db import models

class DesalinationStation(models.Model):
    name = models.CharField(max_length=255)  # Nom de la station
    location = models.CharField(max_length=255)  # Emplacement de la station
    status = models.CharField(
        max_length=20,
        choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Maintenance', 'Maintenance')],
        default='Active'
    )  # Statut de la station
    last_maintenance_date = models.DateTimeField(null=True, blank=True)  # Dernière date de maintenance

    def __str__(self):
        return self.name


from django.db import models

class StationParameters(models.Model):
    station = models.ForeignKey(DesalinationStation, on_delete=models.CASCADE)
    parameter_name = models.CharField(max_length=100,default='unknown')  # Assure-toi que ce champ existe
    value = models.FloatField(default=0.0)  # Assure-toi que ce champ existe
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return f"{self.parameter_name} = {self.value}"

class Alert(models.Model):
    station = models.ForeignKey(DesalinationStation, on_delete=models.CASCADE)
    message = models.CharField(max_length=255,default='')  # Assure-toi que ce champ existe
    alert_type = models.CharField(max_length=50,default='info')
    timestamp = models.DateTimeField(auto_now_add=True)  # Assure-toi que ce champ existe

    def __str__(self):
        return self.message
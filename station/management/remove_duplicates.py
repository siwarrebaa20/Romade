from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db.models.functions import Lower
from station.models import Station

class Command(BaseCommand):
    help = 'Supprime les doublons de stations en ignorant la casse'

    def handle(self, *args, **kwargs):
        # Étape 1: Identifier les doublons en ignorant la casse
        duplicates = Station.objects.annotate(
            normalized_nom=Lower('nom'),  # Normalisation en minuscules pour 'nom'
            normalized_localisation=Lower('localisation')  # Normalisation en minuscules pour 'localisation'
        ).values('normalized_nom', 'normalized_localisation', 'capacite', 'date_installation')\
            .annotate(count=Count('id'))\
            .filter(count__gt=1)

        # Afficher les doublons pour vérification
        self.stdout.write(self.style.SUCCESS("Doublons trouvés :"))
        for duplicate in duplicates:
            self.stdout.write(str(duplicate))

        # Étape 2: Supprimer les doublons (en gardant uniquement un seul élément pour chaque groupe de doublons)
        for duplicate in duplicates:
            # Trouver tous les enregistrements avec les mêmes nom, localisation et capacite, en ignorant la casse
            stations_to_delete = Station.objects.filter(
                nom__iexact=duplicate['normalized_nom'],
                localisation__iexact=duplicate['normalized_localisation'],
                capacite=duplicate['capacite'],
                date_installation=duplicate['date_installation']
            ).order_by('id')  # Ordre d'abord par ID pour garder le premier élément

            # Supprimer tous les doublons sauf le premier
            stations_to_delete[1:].delete()

        # Optionnel: vérifier que les doublons ont bien été supprimés
        remaining_stations = Station.objects.all()
        self.stdout.write(self.style.SUCCESS("Stations restantes après suppression des doublons :"))
        for station in remaining_stations:
            self.stdout.write(str(station))

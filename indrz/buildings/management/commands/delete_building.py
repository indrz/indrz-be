# buildings/management/commands/delete_building.py

from django.core.management.base import BaseCommand
from django.db.models import Q
from buildings.models import BuildingFloor, Wing, Building
from poi_manager.models import Poi

class Command(BaseCommand):
    help = 'Delete a building and related objects'

    def add_arguments(self, parser):
        parser.add_argument('building_name', type=str, help='Name of the building to delete')

    def handle(self, *args, **kwargs):
        building_name = kwargs['building_name']

        Building.objects.filter(Q(building_name__icontains=building_name)).delete()

        # Delete BuildingFloor objects
        BuildingFloor.objects.filter(Q(long_name__icontains=building_name)).delete()

        # Delete Wing objects
        Wing.objects.filter(Q(name__icontains=building_name)).delete()

        # Delete POI entrances
        Poi.objects.filter(Q(name__icontains=building_name) & Q(category_id=13)).delete()

        # Delete POI wings
        Poi.objects.filter(Q(name__icontains=building_name) & Q(category_id=80)).delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted building and related objects for: {building_name}'))
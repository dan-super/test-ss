import csv
import json
import xmltodict
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from poi.models import PointOfInterest

class Command(BaseCommand):
    help = 'Import POI data from CSV, JSON, or XML files'

    def add_arguments(self, parser):
        parser.add_argument('file_paths', nargs='+', type=str, help='Paths to the data files to import')

    def handle(self, *args, **options):
        for file_path in options['file_paths']:
            path = Path(file_path)
            if not path.exists():
                raise CommandError(f'File {file_path} does not exist')

            try:
                if path.suffix.lower() == '.csv':
                    self.import_csv(path)
                elif path.suffix.lower() == '.json':
                    self.import_json(path)
                elif path.suffix.lower() == '.xml':
                    self.import_xml(path)
                else:
                    self.stdout.write(self.style.WARNING(f'Unsupported file type: {path.suffix}'))
            except Exception as e:
                raise CommandError(f'Error importing {file_path}: {str(e)}')

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {file_path}'))

    def import_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                PointOfInterest.objects.update_or_create(
                    external_id=row['poi_id'],
                    defaults={
                        'name': row['poi_name'],
                        'latitude': float(row['poi_latitude']),
                        'longitude': float(row['poi_longitude']),
                        'category': row['poi_category'],
                        'ratings': [float(x) for x in row['poi_ratings'].strip('{}').split(',') if x]
                    }
                )

    def import_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                data = [data]
            
            for item in data:
                PointOfInterest.objects.update_or_create(
                    external_id=item['id'],
                    defaults={
                        'name': item['name'],
                        'latitude': float(item['coordinates']['latitude']),
                        'longitude': float(item['coordinates']['longitude']),
                        'category': item['category'],
                        'ratings': item['ratings'],
                        'description': item.get('description')
                    }
                )

    def import_xml(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = xmltodict.parse(f.read())
            pois = data.get('pois', {}).get('poi', [])
            if isinstance(pois, dict):
                pois = [pois]
            
            for poi in pois:
                PointOfInterest.objects.update_or_create(
                    external_id=poi['pid'],
                    defaults={
                        'name': poi['pname'],
                        'latitude': float(poi['platitude']),
                        'longitude': float(poi['plongitude']),
                        'category': poi['pcategory'],
                        'ratings': json.loads(poi['pratings'])
                    }
                )

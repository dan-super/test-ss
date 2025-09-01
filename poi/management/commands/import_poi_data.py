import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.etree.ElementTree import XMLParser
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
        # Read file content and replace problematic characters
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.replace('&', '&amp;')  # Pre-escape ampersands
        
        parser = XMLParser(encoding='utf-8')
        root = ET.fromstring(content, parser=parser)
        
        for record in root.findall('DATA_RECORD'):
            ratings = [int(x) for x in record.find('pratings').text.split(',') if x]
            PointOfInterest.objects.update_or_create(
                external_id=record.find('pid').text,
                defaults={
                    'name': record.find('pname').text,
                    'latitude': float(record.find('platitude').text),
                    'longitude': float(record.find('plongitude').text),
                    'category': record.find('pcategory').text,
                    'ratings': ratings
                }
            )

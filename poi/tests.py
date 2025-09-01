import json
import tempfile
import os
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import PointOfInterest
from .management.commands.import_poi_data import Command as ImportCommand

class PointOfInterestTests(TestCase):
    def setUp(self):
        self.valid_poi_data = {
            "id": "6166590368",
            "name": "Test POI",
            "category": "convenience-store",
            "description": "Test description",
            "coordinates": {
                "latitude": 48.0082738999357,
                "longitude": 16.2454885
            },
            "ratings": [2, 2, 3, 3, 4, 5, 2, 2, 4, 1]
        }

    def test_poi_creation(self):
        poi = PointOfInterest.objects.create(
            external_id=self.valid_poi_data["id"],
            name=self.valid_poi_data["name"],
            category=self.valid_poi_data["category"],
            latitude=self.valid_poi_data["coordinates"]["latitude"],
            longitude=self.valid_poi_data["coordinates"]["longitude"],
            ratings=self.valid_poi_data["ratings"],
            description=self.valid_poi_data["description"]
        )
        
        self.assertEqual(poi.external_id, "6166590368")
        self.assertEqual(poi.name, "Test POI")
        self.assertEqual(len(poi.ratings), 10)
        self.assertEqual(poi.category, "convenience-store")

    def test_coordinate_validation(self):
        with self.assertRaises(ValidationError):
            poi = PointOfInterest(
                external_id="test",
                name="Test POI",
                category="test",
                latitude=91,
                longitude=0,
                ratings=[]
            )
            poi.full_clean()

        with self.assertRaises(ValidationError):
            poi = PointOfInterest(
                external_id="test",
                name="Test POI",
                category="test",
                latitude=0,
                longitude=181,
                ratings=[]
            )
            poi.full_clean()

    def test_average_rating_calculation(self):
        poi = PointOfInterest.objects.create(
            external_id="test1",
            name="Test POI 1",
            category="test",
            latitude=0,
            longitude=0,
            ratings=[1, 2, 3, 4, 5]
        )
        self.assertEqual(poi.average_rating, 3.0)

        poi = PointOfInterest.objects.create(
            external_id="test2",
            name="Test POI 2",
            category="test",
            latitude=0,
            longitude=0,
            ratings=[]
        )
        self.assertIsNone(poi.average_rating)

    def test_json_import(self):
        test_data = [
            {
                "id": "test1",
                "name": "Test POI 1",
                "category": "test-category",
                "coordinates": {
                    "latitude": 10.0,
                    "longitude": 20.0
                },
                "ratings": [1, 2, 3, 4, 5],
                "description": "Test description"
            },
            {
                "id": "test2",
                "name": "Test POI 2",
                "category": "test-category",
                "coordinates": {
                    "latitude": -10.0,
                    "longitude": -20.0
                },
                "ratings": [5, 4, 3, 2, 1],
                "description": "Another test description"
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(test_data, f)
            temp_file = f.name
        
        try:
            command = ImportCommand()
            command.handle(file_paths=[temp_file])
            
            self.assertEqual(PointOfInterest.objects.count(), 2)
            
            poi1 = PointOfInterest.objects.get(external_id="test1")
            self.assertEqual(poi1.name, "Test POI 1")
            self.assertEqual(poi1.category, "test-category")
            self.assertEqual(poi1.latitude, 10.0)
            self.assertEqual(poi1.longitude, 20.0)
            self.assertEqual(poi1.ratings, [1, 2, 3, 4, 5])
            self.assertEqual(poi1.description, "Test description")
            
            poi2 = PointOfInterest.objects.get(external_id="test2")
            self.assertEqual(poi2.name, "Test POI 2")
            self.assertEqual(poi2.latitude, -10.0)
            self.assertEqual(poi2.longitude, -20.0)
            
        finally:
            os.unlink(temp_file)

    def test_unicode_handling(self):
        poi = PointOfInterest.objects.create(
            external_id="unicode_test",
            name="50嵐",
            category="test",
            latitude=0,
            longitude=0,
            ratings=[]
        )
        self.assertEqual(poi.name, "50嵐")

    def test_duplicate_external_id(self):
        PointOfInterest.objects.create(
            external_id="duplicate_test",
            name="Test POI 1",
            category="test",
            latitude=0,
            longitude=0,
            ratings=[]
        )

        with self.assertRaises(Exception):
            PointOfInterest.objects.create(
                external_id="duplicate_test",
                name="Test POI 2",
                category="test",
                latitude=1,
                longitude=1,
                ratings=[]
            )

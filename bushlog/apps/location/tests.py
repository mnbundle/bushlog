import json

from django.test import TestCase

from bushlog.apps.location.models import Coordinate


class CoordinatesTestCase(TestCase):
    def setUp(self):
        self.object = Coordinate.objects.get(id=1)

    def test_model(self):

        # ensure the object was created correctly
        self.assertIsInstance(self.object, Coordinate)

    def test_as_json(self):
        json_object = self.object.as_json()

        # ensure the json object is returned as a string
        self.assertIsInstance(json_object, str)

        # ensure that the json object is valid
        json.loads(json_object)

    def tearDown(self):
        pass

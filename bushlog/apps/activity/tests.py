from django.test import TestCase

from bushlog.apps.sighting.models import Sighting, SightingImage


class SightingTestCase(TestCase):
    def setUp(self):
        self.object = Sighting.objects.get(id=1)

    def test_model(self):

        # ensure the object was created correctly
        self.assertIsInstance(self.object, Sighting)

    def tearDown(self):
        pass


class SightingImageTestCase(TestCase):
    def setUp(self):
        self.object = SightingImage.objects.get(id=1)

    def test_model(self):

        # ensure the object was created correctly
        self.assertIsInstance(self.object, SightingImage)

    def tearDown(self):
        pass

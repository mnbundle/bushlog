from django.test import TestCase

from bushlog.apps.wildlife.models import Species, SpeciesInfo


class SpeciesTestCase(TestCase):
    def setUp(self):
        self.object = Species.objects.get(id=1)

    def test_model(self):

        # ensure the object was created correctly
        self.assertIsInstance(self.object, Species)

    def tearDown(self):
        pass


class SpeciesInfoTestCase(TestCase):
    def setUp(self):
        self.object = SpeciesInfo.objects.get(id=1)

    def test_model(self):

        # ensure the object was created correctly
        self.assertIsInstance(self.object, SpeciesInfo)

    def tearDown(self):
        pass

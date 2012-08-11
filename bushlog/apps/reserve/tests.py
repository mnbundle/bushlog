from django.test import TestCase

from bushlog.apps.reserve.models import Reserve


class ReserveTestCase(TestCase):
    def setUp(self):
        self.object = Reserve.objects.get(id=1)

    def test_model(self):

        # ensure the object was created correctly
        self.assertIsInstance(self.object, Reserve)

    def tearDown(self):
        pass

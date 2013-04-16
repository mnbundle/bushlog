from django.test import TestCase

from bushlog.apps.like.models import Like


class LikeTestCase(TestCase):
    def setUp(self):
        self.object = Like.objects.get(id=1)

    def test_model(self):

        # ensure the object was created correctly
        self.assertIsInstance(self.object, Like)

    def tearDown(self):
        pass

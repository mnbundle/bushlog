from django.test import TestCase

from bushlog.apps.profile.models import Notification


class NotificationTestCase(TestCase):
    def setUp(self):
        self.object = Notification.objects.get(id=1)

    def test_model(self):

        # ensure the object was created correctly
        self.assertIsInstance(self.object, Notification)

    def tearDown(self):
        pass

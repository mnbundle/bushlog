from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = 'username'
    help = "Get a users activation url by username."

    def handle(self, *args, **options):
        """
        Outputs an activiation url for a given username.
        """
        try:
            username = args[0]
        except IndexError:
            exit("Username needs to be provided as an arg.")

        user = User.objects.get(username=username)

        print "Activation url: %s/profile/activation/?uid=%s&token=%s&activate=activate" % (
            settings.HOST,
            user.id,
            user.profile.token
        )

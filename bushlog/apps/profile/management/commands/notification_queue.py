from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse_lazy

from bushlog.apps.profile.models import Notification


class Command(BaseCommand):
    args = ''
    help = "Send user notiications of any type."

    def handle(self, *args, **options):
        """
        Iterate through all records send the notification and remove the user.
        """
        for obj in Notification.objects.all():
            for user in obj.user.all():
                if obj.type == 'activate_profile':
                    activation_link = "%s%s?uid=%s&token=%s" % (
                        settings.HOST, reverse_lazy('profile:activate'), user.id, user.profile.token
                    )
                    if obj.send(to=[user.email], activation_link=activation_link):
                        obj.user.remove(user)
                elif obj.type == 'reset_password':
                    reset_link = "%s%s?uid=%s&token=%s" % (
                        settings.HOST, reverse_lazy('profile:reset_password_redirect'), user.id, user.profile.token
                    )
                    if obj.send(to=[user.email], reset_link=reset_link):
                        obj.user.remove(user)

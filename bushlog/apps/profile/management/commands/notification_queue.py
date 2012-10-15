from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from bushlog.apps.profile import Notification


class Command(BaseCommand):
    args = ''
    help = "Send user notiications of any type."

    def handle(self, *args, **options):
        obj_list = Notification.objects.all()

        # iterate through all records and delete them
        for obj in obj_list:
            for user in obj.user.all():
                if obj.type == 'activate_profile':
                    activation_link = ""
                    obj.send(to=[user.email], activation_link=activation_link)
                elif obj.type == 'reset_password':
                    reset_link = ""
                    obj.send(to=[user.email], reset_link=reset_link)

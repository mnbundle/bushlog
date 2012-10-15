from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.db import models

from bushlog.apps.location.models import Country
from bushlog.utils import choices


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    biography = models.CharField(max_length=250, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", max_length=250, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=choices(['Male', 'Female']), blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.ForeignKey(Country, related_name='users', blank=True, null=True)

    @property
    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def add_notification(self, notification_type):
        """
        Adds a notification by type to be processed via a cronjob and management command.
        """
        self.user.notifications.add(
            Notification.objects.get(type=notification_type)
        )
        self.save()

    def __unicode__(self):
        return self.user.username


class Notification(models.Model):
    user = models.ManyToManyField(User, related_name="notifications", blank=True, null=True)
    type = models.CharField(max_length=20, choices=choices(['activate_profile', 'reset_password']), unique=True)
    subject = models.CharField(max_length=75)
    body = models.TextField()

    def send(self, to=[], *args, **kwargs):
        """
        Sends a confirmation email to a list of users. Note the use of str formatting.
        """
        email_msg = EmailMessage(
            subject=self.subject,
            body=self.body.format(kwargs),
            from_email=settings.FROM_EMAIL,
            to=to
        )

        try:
            email_msg.send(fail_silently=False)
            return True
        except:
            return False


User.profile = property(
    lambda user: UserProfile.objects.get_or_create(user=user)[0]
)

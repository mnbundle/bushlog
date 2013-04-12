import hashlib
from os import path

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.db import models
from django.template import Context
from django.template.loader import get_template

from bushlog.apps.location.models import Country
from bushlog.utils import choices, random_string


def uploadpath(instance, filename):
    return "%s.jpg" % path.join('avatars', instance.slug, random_string())


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    slug = models.SlugField()
    biography = models.CharField(max_length=250, blank=True, null=True)
    avatar = models.ImageField(upload_to=uploadpath, max_length=250, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=choices(['Male', 'Female']), blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.ForeignKey(Country, related_name='user_profile', blank=True, null=True)

    @property
    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    @property
    def token(self):
        return hashlib.md5("%s:%s:%s" % (self.user.id, self.user.password, settings.SECRET_KEY)).hexdigest()

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
    template = models.CharField(max_length=100)

    def send(self, to=[], *args, **kwargs):
        """
        Sends a notification email to users. Note the use of str formatting.
        """
        # format the body text to include all kwargs
        email_body = self.body.format(**kwargs)

        # form the html template and it's context into a html str
        html_template = get_template(self.template)
        html_context = Context({'obj': self, 'settings': settings})
        html_context.update(kwargs)
        html_content = html_template.render(html_context)

        # initiates the email message and attaches the html alternative
        email_msg = EmailMultiAlternatives(
            subject=self.subject,
            body=email_body,
            from_email=settings.FROM_EMAIL,
            to=to
        )
        email_msg.attach_alternative(html_content, "text/html")

        # if the send fails return false
        try:
            if settings.DEBUG:
                print email_msg.message()
            else:
                email_msg.send(fail_silently=False)
            return True
        except:
            return False


User.profile = property(
    lambda user: UserProfile.objects.get_or_create(user=user, slug=user.username)[0]
)

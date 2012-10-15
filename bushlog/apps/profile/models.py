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

    def __unicode__(self):
        return self.user.username


User.profile = property(
    lambda user: UserProfile.objects.get_or_create(user=user)[0]
)

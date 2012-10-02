from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    alias = models.SlugField()

    @property
    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def __unicode__(self):
        return self.user.username


User.profile = property(
    lambda user: UserProfile.objects.get_or_create(user=user)[0]
)

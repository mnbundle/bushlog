from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    alias = models.SlugField()


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

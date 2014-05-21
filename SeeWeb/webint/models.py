# This is an auto-generated Django model module.

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    position = models.CharField(max_length=250)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
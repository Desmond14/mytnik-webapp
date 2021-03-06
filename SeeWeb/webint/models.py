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

class RuleStorage(models.Model):
    instance_name = models.CharField(max_length=255, unique=True)
    instance_description = models.CharField(max_length=512)
    json_file = models.FileField(upload_to='rules')

    def __unicode__(self):
        return self.instance_name

    def url_name(self):
        return self.instance_name.replace(' ', '_')
class ContainerStatus(models.Model):
    assignee = models.ForeignKey(User, blank=True, null=True)

    container_id = models.CharField(max_length=100)

    STATUS_CHOICES = (
    ("NA", "Not assigned"),
    ("IP", "In progress"),
    ("DO", "Done"),
    )
    status = models.CharField(max_length=2,
                              choices=STATUS_CHOICES,
                              default="NA")

    def __str__(self):
        return "ContainerID:" + self.container_id + ", status: " + self.status + " " + self.user.username
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Connection(TimeStampedModel):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    connection_url = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=False)
    library = models.CharField(max_length=100, blank=True, null=True)
    class_str = models.CharField(max_length=100, blank=True, null=True)

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url

    def user_connected(self, user_id):
        if self.userconnection_set.filter(user_id=user_id).count() > 0:
            return True
        return False


class UserConnection(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

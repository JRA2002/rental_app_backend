from django.db import models
from django.contrib.auth.models import User

class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    DNI = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


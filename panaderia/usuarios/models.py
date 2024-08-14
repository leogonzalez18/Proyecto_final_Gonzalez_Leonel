from django.db import models
from django.contrib.auth.models import User

class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='avatars', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user} - {self.image}"
    
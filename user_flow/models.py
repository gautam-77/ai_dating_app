from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    active_status = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name
    
class Imagetotext(models.Model):
    image_text = models.CharField(max_length=100)
    image_file = models.FileField(upload_to='imagetext')    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.user.name
    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="userprofile")   
    city = models.CharField(max_length=20)
    link = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.user.name
    
class CustomToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return get_random_string(40)    
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"

class Todo(models.Model):
    user = models.ForeignKey(User, blank=False, related_name='todo',on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, blank=False)

    def __str__(self) :
        return f'{self.user}: {self.content}'
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Feature(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='features/')  # Uploads images to media/features/

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)  # Admin approval flag
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('user', 'User'), ('doctor', 'Doctor')], default='user')

    def __str__(self):
        return self.name

from django.db import models

class DialysisCenter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    full_address = models.TextField()
    district = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    id = models.AutoField(primary_key = True)
    hosp_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.hosp_name

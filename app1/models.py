from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class Feature(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='features/')

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
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

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    phone_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=10, default="Yes")

    def __str__(self):
        return f"{self.name} - {self.specialization}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'user':
        UserProfile.objects.create(user=instance)

class Appointment(models.Model):
    TIMING_CHOICES = [
        ('Forenoon', 'Forenoon'),
        ('Afternoon', 'Afternoon'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, default=None)

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    date = models.DateField()
    timing = models.CharField(max_length=20, choices=TIMING_CHOICES)
    status = models.CharField(max_length=20, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.doctor.name} - {self.date}"

from django.db import models
from django.utils.text import slugify

class Stage(models.Model):
    title = models.CharField(max_length=100, unique=False)
    short_description = models.TextField()
    detailed_description = models.TextField()
    image = models.ImageField(upload_to='stage_images/')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class DietPlan(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='diet_plans')
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    detailed_instructions = models.TextField()
    image = models.ImageField(upload_to='diet_images/')
    video_url = models.URLField(blank=True, null=True)  # Optional YouTube video etc.

    def __str__(self):
        return f"{self.title} ({self.stage.title})"

class WorkoutPlan(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='workout_plans')
    title = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)  # e.g., "15 minutes"
    image = models.ImageField(upload_to='workout_images/')
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} ({self.stage.title})"

from django.db import models

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

from django.db import models

# Create your models here.
class Mood(models.Model):
    mood = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mood}"
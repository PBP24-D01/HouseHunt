from django.db import models
from django.contrib.auth import User
from rumah.models import House

# Create your models here.

class Wishlist(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rumah = models.ForeignKey(House, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='medium')

    def __str__(self):
        return f"{self.user.username} - {self.house.title} ({self.get_priority_display()})"
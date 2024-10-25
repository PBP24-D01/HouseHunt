from django.db import models
from django.conf import settings
from rumah.models import House
from django.core.exceptions import ValidationError

# Create your models here.

class Wishlist(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rumah = models.ForeignKey(House, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='medium')

    def __str__(self):
        return f"{self.user.username} - {self.rumah.judul} ({self.get_priority_display()})"

    def clean(self):
        if not self.user.is_buyer:
            raise ValidationError("Only users with buyer status can add houses to the wishlist.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

from django.forms import ValidationError
from HouseHuntAuth.models import Seller, Buyer
from django.db import models
# from django.utils import timezone
from rumah.models import House


class Availability(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='availabilities')
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='availabilities')
    available_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.seller.user.username} - {self.available_date} ({self.start_time} to {self.end_time})"
    
    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('canceled', 'Canceled'),
    ]

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='appointments')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='appointments')
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes_to_seller = models.TextField(blank=True, null=True)

    def __str__(self):
         return f"Appointment between {self.buyer.user.username} and {self.seller.user.username} on {self.availability.available_date}"

    def cancel(self):
       self.status = 'canceled'
       self.save()

    def approve(self):
         self.status = 'approved'
         self.save()

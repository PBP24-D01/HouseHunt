# from django.contrib.auth.models import User
from django.db import models
# from django.utils import timezone
from rumah import House


# # waiting for it to be implemented
class SellerProfile(models.Model):
#     # Extending User to represent a seller
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     # extra fields maybe, contact information, address, etc.


# # waiting for it to be implemented
class BuyerProfile(models.Model):
    # Extending User to represent a buyer
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Availability(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='availabilities')
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='availabilities')
    available_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.seller.user.username} - {self.available_date} ({self.start_time} to {self.end_time})"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('canceled', 'Canceled'),
    ]

    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name='appointments')
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='appointments')
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes_to_seller = models.TextField()

    def __str__(self):
         return f"Appointment between {self.buyer.user.username} and {self.seller.user.username} on {self.appointment_date}"

    def cancel(self):
       self.status = 'canceled'
       self.save()

    def approve(self):
         self.status = 'approved'
         self.save()

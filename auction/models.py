import datetime
import pytz
from django.db import models
from HouseHuntAuth.models import Buyer, Seller
from rumah.models import House
import uuid
# Create your models here.


class Auction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    starting_price = models.PositiveIntegerField(null=False)
    current_price = models.PositiveIntegerField(null=False)
    highest_buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def is_active(self):
        utc = pytz.UTC
        return self.start_date < utc.localize(datetime.datetime.now()) < self.end_date
    
    def is_expired(self):
        utc = pytz.UTC
        return self.end_date < utc.localize(datetime.datetime.now())

class Bid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.auction.title} - {self.buyer.user.username} - {self.price}"
    
    def save(self, *args, **kwargs):
        self.auction.current_price = self.price
        self.auction.highest_buyer = self.buyer
        self.auction.save()
        super().save(*args, **kwargs)
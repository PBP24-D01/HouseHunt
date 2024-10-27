from django.db import models
import uuid
from rumah.models import House
from django.conf import settings
from HouseHuntAuth.models import Seller

class IklanEntry(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    rumah = models.ForeignKey(House, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    banner = models.ImageField(upload_to='banner/')

    def save(self, *args, **kwargs):
        if self.pk:
            old_banner = IklanEntry.objects.get(pk=self.pk)
            if old_banner.banner != self.banner:
                old_banner.banner.delete(save=False)
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.banner.delete(save=False)  
        super().delete(*args, **kwargs)

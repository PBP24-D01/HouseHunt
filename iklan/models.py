from django.db import models
import uuid
from rumah.models import House

class IklanEntry(models.Model):
    rumah = models.ForeignKey(House, on_delete=models.CASCADE)
    id_rumah = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    banner = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk:
            old_banner = Event.objects.get(pk=self.pk)
            if old_banner.banner != self.banner:
                old_banner.banner.delete(save=False)
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.banner.delete(save=False)  
        super().delete(*args, **kwargs)

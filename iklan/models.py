from django.db import models

class IklanEntry(models.Model):
    id_rumah = models.UUIDField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    banner = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        if self.pk:
            old_banner = Event.objects.get(pk=self.pk)
            if old_banner.banner != self.banner:
                old_banner.banner.delete(save=False)
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.banner.delete(save=False)
        super().delete(*args, **kwargs)

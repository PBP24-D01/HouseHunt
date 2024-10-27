from django.db import models
from django.core.validators import MinValueValidator
import os 

# Create your models here.

class House(models.Model):
    judul = models.CharField(max_length=100)
    deskripsi = models.CharField(max_length=255)
    harga = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    lokasi = models.CharField(max_length=100)
    gambar = models.ImageField(upload_to='static/img/')
    kamar_tidur = models.IntegerField(validators=[MinValueValidator(1)])
    kamar_mandi = models.IntegerField(validators=[MinValueValidator(1)])
    is_available = models.BooleanField(default=True)  
    seller = models.ForeignKey('HouseHuntAuth.Seller', on_delete=models.CASCADE)

    def __str__(self):
        return self.judul
    
    def delete(self, *args, **kwargs):
        if self.gambar:
            if os.path.isfile(self.gambar.path):
                os.remove(self.gambar.path)
        super().delete(*args, **kwargs)
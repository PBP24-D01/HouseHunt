from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

class House(models.Model):
    judul = models.CharField(max_length=100)
    deskripsi = models.CharField
    harga = models.DecimalField(max_digits= None,decimal_places=None, validators=[MinValueValidator(0.1)]  ) # sesuaiin dah ntr
    lokasi = models.CharField(max_length=100)
    gambar = models.ImageField(upload_to='/static/img')
    kamar_tidur = models.IntegerField(validators=[MinValueValidator(1)])
    kamar_mandi = models.IntegerField(validators=[MinValueValidator(1)])
    is_available = models.BooleanField(default=True)  
    seller = models.ForeignKey(User, on_delete=models.CASCADE) # get seller from??

    def __str__(self):
        return self.title

class Profile(models.Model):
    ROLE_CHOICES = (
        ('penjual', 'Penjual'),
        ('pembeli', 'Pembeli'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=7, choices=ROLE_CHOICES, default='pembeli')

    def __str__(self):
        return self.user.username  
    
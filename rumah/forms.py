from django import forms
from .models import House

class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields =['judul','deskripsi','harga','lokasi','gambar','kamar_tidur','kamar_mandi','is_available','seller']
        
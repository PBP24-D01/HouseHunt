from django import forms
from .models import House, Profile  

class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields =['judul','deskripsi','harga','lokasi','gambar','kamar_tidur','kamar_mandi','is_available','seller']
        
class ProfileForm(forms.ModelForm): # User type adjust later
    class Meta:
        model = Profile
        fields = ['user','user_type']
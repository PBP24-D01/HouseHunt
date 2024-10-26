from django import forms
from .models import House  

class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields =['judul','deskripsi','harga','lokasi','gambar','kamar_tidur','kamar_mandi','is_available']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'form-input rounded-md'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-textarea rounded-md'}),
            'harga': forms.NumberInput(attrs={'class': 'form-input rounded-md'}),
            'lokasi': forms.TextInput(attrs={'class': 'form-input rounded-md'}),
            'gambar': forms.FileInput(attrs={'class': 'form-input rounded-md'}),
            'kamar_tidur': forms.NumberInput(attrs={'class': 'form-input rounded-md'}),
            'kamar_mandi': forms.NumberInput(attrs={'class': 'form-input rounded-md'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'seller': forms.Select(attrs={'class': 'form-select rounded-md'}),
        }
        
class HouseFilterForm(forms.Form):
    PRICE_CHOICES = [ # double check later plz
        ('', 'Semua Harga'),
        ('0-500000000', 'Dibawah 500 Juta'),
        ('500000000-1000000000', '500 Juta - 1 Miliar'), 
        ('1000000000-2000000000', '1 Miliar - 2 Miliar'),
        ('2000000000-999999999999', 'Diatas 2 Miliar')
    ]
    
    BEDROOM_CHOICES = [
        ('', 'Semua'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4+', '4+')
    ]
    
    BATHROOM_CHOICES = [
        ('', 'Semua'),
        ('1', '1'),
        ('2', '2'),
        ('3+', '3+')
    ]

    LOCATION_CHOICES = [
        ('', 'Semua'),
        ('Babelan', 'Babelan'),
        ('Bantar Gebang', 'Bantar Gebang'),
        ('Bekasi', 'Bekasi'),
        ('Bekasi Barat', 'Bekasi Barat'),
        ('Bekasi Kota', 'Bekasi Kota'),
        ('Bekasi Timur', 'Bekasi Timur'),
        ('Bekasi Utara', 'Bekasi Utara'),
        ('Bintara', 'Bintara'),
        ('Caman', 'Caman'),
        ('Cibitung', 'Cibitung'),
        ('Cibubur', 'Cibubur'),
        ('Cikarang', 'Cikarang'),
        ('Cikarang Selatan', 'Cikarang Selatan'),
        ('Cikunir', 'Cikunir'),
        ('Cimuning', 'Cimuning'),
        ('Duren Jaya', 'Duren Jaya'),
        ('Duta Harapan', 'Duta Harapan'),
        ('Galaxy', 'Galaxy'),
        ('Golden City', 'Golden City'),
        ('Grand Wisata', 'Grand Wisata'),
        ('Harapan Baru', 'Harapan Baru'),
        ('Harapan Indah', 'Harapan Indah'),
        ('Harapan Jaya', 'Harapan Jaya'),
        ('Harapan Mulya', 'Harapan Mulya'),
        ('Jababeka', 'Jababeka'),
        ('Jaka Sampurna', 'Jaka Sampurna'),
        ('Jatibening', 'Jatibening'),
        ('Jati Asih', 'Jati Asih'),
        ('Jati Cempaka', 'Jati Cempaka'),
        ('Jati Luhur', 'Jati Luhur'),
        ('Jati Mekar', 'Jati Mekar'),
        ('Jatiwarna', 'Jatiwarna'),
        ('Jatikramat', 'Jatikramat'),
        ('Jatimakmur', 'Jatimakmur'),
        ('Jatimurni', 'Jatimurni'),
        ('Jatiraden', 'Jatiraden'),
        ('Jatiranggon', 'Jatiranggon'),
        ('Jatisampurna', 'Jatisampurna'),
        ('Jatiwaringin', 'Jatiwaringin'),
        ('Kaliabang', 'Kaliabang'),
        ('Karang Satria', 'Karang Satria'),
        ('Kayuringin Jaya', 'Kayuringin Jaya'),
        ('Kebalen', 'Kebalen'),
        ('Kemang Pratama', 'Kemang Pratama'),
        ('Komsen', 'Komsen'),
        ('Kranji', 'Kranji'),
        ('Margahayu', 'Margahayu'),
        ('Medan Satria', 'Medan Satria'),
        ('Mustika Jaya', 'Mustika Jaya'),
        ('Mustikasari', 'Mustikasari'),
        ('Narongong', 'Narongong'),
        ('Pekayon', 'Pekayon'),
        ('Pedurenan', 'Pedurenan'),
        ('Pejuang', 'Pejuang'),
        ('Perwira', 'Perwira'),
        ('Pondok Gede', 'Pondok Gede'),
        ('Pondok Melati', 'Pondok Melati'),
        ('Pondok Ungu', 'Pondok Ungu'),
        ('Rawalumbu', 'Rawalumbu'),
        ('Satria Jaya', 'Satria Jaya'),
        ('Serang Baru', 'Serang Baru'),
        ('Setu', 'Setu'),
        ('Summarecon', 'Summarecon'),
        ('Tambun Selatan', 'Tambun Selatan'),
        ('Tambung Utara', 'Tambung Utara'),
        ('Tanah Tinggi', 'Tanah Tinggi'),
        ('Tarumajaya', 'Tarumajaya')
    ]
    
    price_range = forms.ChoiceField(
        choices=PRICE_CHOICES, 
        required=False, 
        label='Rentang Harga',
        widget=forms.Select(attrs={'class': 'form-select rounded-md'})
    )
    
    lokasi = forms.ChoiceField(
        choices=LOCATION_CHOICES,
        required=False, 
        label='Lokasi',
        widget=forms.Select(attrs={'class': 'form-input rounded-md'})
    )
    
    kamar_tidur = forms.ChoiceField(
        choices=BEDROOM_CHOICES, 
        required=False, 
        label='Kamar Tidur',
        widget=forms.Select(attrs={'class': 'form-select rounded-md'})
    )
    
    kamar_mandi = forms.ChoiceField(
        choices=BATHROOM_CHOICES, 
        required=False, 
        label='Kamar Mandi',
        widget=forms.Select(attrs={'class': 'form-select rounded-md'})
    )
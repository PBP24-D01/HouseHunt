from django.test import TestCase, Client
from django.urls import reverse
from HouseHuntAuth.models import CustomUser, Seller, Buyer
from .models import House
from .forms import HouseForm
from django.core.files.uploadedfile import SimpleUploadedFile
import requests

# URL of a small valid image
image_url = 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png' # Harusnya ga di rate limit(?)

def get_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    return response.content

class HouseModelTest(TestCase):
    def setUp(self):
        self.seller_user = CustomUser.objects.create_user(username='seller', password='password')
        self.seller = Seller.objects.create(
            user=self.seller_user,
            company_name='Test Company',
            company_address='123 Test Street',
        )
        image_content = get_image_from_url(image_url)
        self.image = SimpleUploadedFile(name='test_image.png', content=image_content, content_type='image/png')
        self.house = House.objects.create(
            judul='Test House',
            deskripsi='Test Description',
            harga=1000000,
            lokasi='Bekasi',  
            gambar=self.image,
            kamar_tidur=3,
            kamar_mandi=2,
            is_available=True,
            seller=self.seller
        )

    def test_house_creation(self):
        self.assertEqual(self.house.judul, 'Test House')
        self.assertEqual(self.house.deskripsi, 'Test Description')
        self.assertEqual(self.house.harga, 1000000)
        self.assertEqual(self.house.lokasi, 'Bekasi')  
        self.assertEqual(self.house.kamar_tidur, 3)
        self.assertEqual(self.house.kamar_mandi, 2)
        self.assertTrue(self.house.is_available)
        self.assertEqual(self.house.seller, self.seller)

class HouseFormTest(TestCase):
    def test_1_house_form_valid(self):
        image_content = get_image_from_url(image_url)
        image = SimpleUploadedFile(name='test_image.png', content=image_content, content_type='image/png')
        form_data = {
            'judul': 'Test House',
            'deskripsi': 'Test Description',
            'harga': 1000000,
            'lokasi': 'Bekasi',  
            'gambar': image,
            'kamar_tidur': 3,
            'kamar_mandi': 2,
            'is_available': True
        }
        form = HouseForm(data=form_data, files={'gambar': image})
        self.assertTrue(form.is_valid(), form.errors)

    def test_2_house_form_invalid(self):
        form_data = {
            'judul': '',
            'deskripsi': 'Test Description',
            'harga': 1000000,
            'lokasi': '',  
            'gambar': 'test.jpg',
            'kamar_tidur': 3,
            'kamar_mandi': 2,
            'is_available': True
        }
        form = HouseForm(data=form_data)
        self.assertFalse(form.is_valid())

class HouseViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller_user = CustomUser.objects.create_user(username='seller', password='password')
        self.seller = Seller.objects.create(
            user=self.seller_user,
            company_name='Test Company',
            company_address='123 Test Street',
        )
        image_content = get_image_from_url(image_url)
        self.image = SimpleUploadedFile(name='test_image.png', content=image_content, content_type='image/png')
        self.house = House.objects.create(
            judul='Test House',
            deskripsi='Test Description',
            harga=1000000,
            lokasi='Bekasi',  
            gambar=self.image,
            kamar_tidur=3,
            kamar_mandi=2,
            is_available=True,
            seller=self.seller
        )

    def test_3_landing_page(self):
        response = self.client.get(reverse('houses:landing_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')

    def test_4_house_detail_view(self):
        response = self.client.get(reverse('houses:house_detail', args=[self.house.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'house_detail.html')

    def test_5_house_create_view(self):
        self.client.login(username='seller', password='password')
        image_content = get_image_from_url(image_url)
        image = SimpleUploadedFile(name='new_image.png', content=image_content, content_type='image/png')
        form_data = {
            'judul': 'New House',
            'deskripsi': 'New Description',
            'harga': 2000000,
            'lokasi': 'Bekasi',  
            'gambar': image,
            'kamar_tidur': 4,
            'kamar_mandi': 3,
            'is_available': True
        }
        response = self.client.post(reverse('houses:house_create'), data=form_data, files={'gambar': image})
        if response.status_code != 302:
            print(response.context['form'].errors)  
        self.assertEqual(response.status_code, 302) 

    def test_6_house_edit_view(self):
        self.client.login(username='seller', password='password')
        image_content = get_image_from_url(image_url)
        image = SimpleUploadedFile(name='updated_image.png', content=image_content, content_type='image/png')
        form_data = {
            'judul': 'Updated House',
            'deskripsi': 'Updated Description',
            'harga':3000000,
            'lokasi': 'Bekasi', 
            'gambar': image,
            'kamar_tidur': 5,
            'kamar_mandi': 4,
            'is_available': False
        }
        response = self.client.post(reverse('houses:house_edit', args=[self.house.id]), data=form_data, files={'gambar': image})
        if response.status_code != 302:
            print(response.context['form'].errors)  
        self.assertEqual(response.status_code, 302)  

    def test_7_house_delete_view(self):
        self.client.login(username='seller', password='password')
        response = self.client.post(reverse('houses:house_delete', args=[self.house.id]))
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(House.objects.filter(id=self.house.id).exists())

class HousePurchaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller_user = CustomUser.objects.create_user(username='seller', password='password')
        self.seller = Seller.objects.create(
            user=self.seller_user,
            company_name='Test Company',
            company_address='123 Test Street',
        )
        self.buyer_user = CustomUser.objects.create_user(username='buyer', password='password')
        self.buyer = Buyer.objects.create(
            user=self.buyer_user,
        )
        image_content = get_image_from_url(image_url)
        self.image = SimpleUploadedFile(name='test_image.png', content=image_content, content_type='image/png')
        self.house = House.objects.create(
            judul='Test House',
            deskripsi='Test Description',
            harga=1000000,
            lokasi='Bekasi',  
            gambar=self.image,
            kamar_tidur=3,
            kamar_mandi=2,
            is_available=True,
            seller=self.seller
        )

    def test_8_order_house(self):
        self.client.login(username='buyer', password='password')
        response = self.client.get(reverse('houses:order_page', args=[self.house.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_page.html')

        response = self.client.get(reverse('houses:generate_invoice', args=[self.house.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoice.html')

        self.house.refresh_from_db()
        self.assertFalse(self.house.is_available)

    def test_9_order_unavailable_house(self):
        self.house.is_available = False
        self.house.save()

        self.client.login(username='buyer', password='password')
        response = self.client.get(reverse('houses:order_page', args=[self.house.id]))
        self.assertRedirects(response, reverse('houses:house_detail', args=[self.house.id]))  # Should redirect to house detail page

        response = self.client.get(reverse('houses:generate_invoice', args=[self.house.id]))
        self.assertRedirects(response, reverse('houses:house_detail', args=[self.house.id]))  # Should redirect to house detail page
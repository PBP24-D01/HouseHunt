from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from iklan.models import IklanEntry
from rumah.models import House
from datetime import datetime
from django.contrib.auth.models import User


class IklanViewTests(TestCase):

    def setUp(self):
        # Create test user and seller profile
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')
        
        # Create house object for testing
        self.house = House.objects.create(name="Test House", seller=self.user.seller)

    def test_add_iklan_ajax_success(self):
        # Define data for the AJAX request
        data = {
            'rumah': self.house.id,
            'start_date': '2024-10-01 00:00',
            'end_date': '2024-10-15 00:00',
            'banner': 'Test Banner'
        }
        
        # Send POST request to the add_iklan_ajax view
        response = self.client.post(reverse('iklan:add_iklan_ajax'), data, content_type='application/json')
        
        # Check if response is JSON and success is True
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})
        
        # Verify the IklanEntry has been created in the database
        self.assertTrue(IklanEntry.objects.filter(rumah=self.house, seller=self.user.seller).exists())

    def test_create_iklan_view_authenticated(self):
        response = self.client.get(reverse('iklan:create_iklan'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_iklan.html')

    def test_create_iklan_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('iklan:create_iklan'))
        self.assertNotEqual(response.status_code, 200)

    def test_show_iklan_view(self):
        response = self.client.get(reverse('iklan:show_iklan'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'iklan.html')

    def test_delete_iklan_view(self):
        # Create an IklanEntry to be deleted
        iklan_entry = IklanEntry.objects.create(
            rumah=self.house,
            seller=self.user.seller,
            start_date=datetime.now(),
            end_date=datetime.now()
        )
        response = self.client.post(reverse('iklan:delete_iklan', args=[iklan_entry.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertFalse(IklanEntry.objects.filter(pk=iklan_entry.id).exists())

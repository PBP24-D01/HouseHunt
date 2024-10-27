from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rumah.models import House
from wishlist.models import Wishlist
from HouseHuntAuth.models import Seller

# Create your tests here.

User = get_user_model()

class WishlistViewsTest(TestCase):
    def setUp(self):
        User = get_user_model()
        
        # Create seller user and buyer user
        self.seller_user, created = User.objects.get_or_create(username='seller')
        self.seller_user.set_password('password')  # Hash the password
        self.seller_user.is_seller = True
        self.seller_user.save()

        self.buyer_user, created = User.objects.get_or_create(username='buyer')
        self.buyer_user.set_password('password')  # Hash the password
        self.buyer_user.is_buyer = True
        self.buyer_user.save()

        # Create a Seller instance and link it to the seller_user
        self.seller, created = Seller.objects.get_or_create(user=self.seller_user)

        # Assign the buyer_user to self.user
        self.user = self.buyer_user

        # Log in the buyer user
        self.client.login(username='buyer', password='password')

        # Create a house
        self.house = House.objects.create(
            judul='Test House',
            deskripsi='A test house',
            harga=100000,
            lokasi='Test Location',
            gambar='path/to/image.jpg',  # This should be a valid path for your tests
            kamar_tidur=2,
            kamar_mandi=1,
            seller=self.seller
        )

    def test_add_wishlist(self):
        # No need to log in again since it's already done in setUp
        response = self.client.post(reverse('add_wishlist', args=[self.house.id]))  # Make sure the request is sent correctly
        
        # Check for 200 OK status for successful addition
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}. Response content: {response.content}")

        # Ensure the item was created
        self.assertTrue(Wishlist.objects.filter(user=self.user, rumah=self.house).exists(), "Wishlist item not found in database.")

    def test_delete_wishlist(self):
        Wishlist.objects.create(user=self.user, rumah=self.house)
        response = self.client.post(reverse('delete_wishlist', args=[self.house.id]))
        self.assertEqual(response.status_code, 302)  # Expect a redirect after deletion
        self.assertFalse(Wishlist.objects.filter(user=self.user, rumah=self.house).exists())

    def test_edit_wishlist(self):
        # Create a wishlist item
        wishlist_item = Wishlist.objects.create(user=self.user, rumah=self.house)
        response = self.client.post(reverse('edit_wishlist', args=[self.house.id]), {'priority': 'high'})
        self.assertEqual(response.status_code, 302)  # Assuming redirect after a successful edit
        wishlist_item.refresh_from_db()
        self.assertEqual(wishlist_item.priority, 'high')

    def test_show_wishlist(self):
        response = self.client.get(reverse('wishlistpage'))
        self.assertEqual(response.status_code, 200)  # Expect 200 OK when the buyer is logged in
        self.assertContains(response, 'Wishlist Rumah Saya')  # Check that the expected content is rendered

    def test_show_wishlist_for_non_buyer(self):
        # Log in a non-buyer user
        non_buyer_user = User.objects.create_user(username='non_buyer', password='password', is_buyer=False)
        self.client.login(username='non_buyer', password='password')

        response = self.client.get(reverse('wishlistpage'))
        self.assertEqual(response.status_code, 403)  # Expect 403 Forbidden for non-buyers
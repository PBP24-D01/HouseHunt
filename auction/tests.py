from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from .models import Auction, Bid
from .forms import AuctionForm
from rumah.models import House
from HouseHuntAuth.models import Buyer, Seller, CustomUser
import json

class AuctionModelTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = CustomUser.objects.create_user(username='seller1', password='test123')
        self.user2 = CustomUser.objects.create_user(username='buyer1', password='test123')
        
        # Create seller and buyer
        self.seller = Seller.objects.create(user=self.user1)
        self.buyer = Buyer.objects.create(user=self.user2)
        
        # Create a test house
        self.house = House.objects.create(
            judul="Test House",
            lokasi="Test Location",
            deskripsi="Test Description",
            gambar="static/img/logo.png",
            kamar_tidur=2,
            kamar_mandi=1,
            harga=1000000,
            is_available=True,
            seller=self.seller
        )
        
        # Create a test auction
        self.auction = Auction.objects.create(
            title="Test Auction",
            house=self.house,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=7),
            starting_price=100000,
            current_price=100000,
            seller=self.seller
        )

    def test_auction_str(self):
        self.assertEqual(str(self.auction), "Test Auction")

    def test_auction_is_active(self):
        self.assertTrue(self.auction.is_active())
        
        # Test inactive auction (future start date)
        future_auction = Auction.objects.create(
            title="Future Auction",
            house=self.house,
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=7),
            starting_price=100000,
            current_price=100000,
            seller=self.seller
        )
        self.assertFalse(future_auction.is_active())

    def test_auction_is_expired(self):
        self.assertFalse(self.auction.is_expired())
        
        # Test expired auction
        past_auction = Auction.objects.create(
            title="Past Auction",
            house=self.house,
            start_date=timezone.now() - timedelta(days=7),
            end_date=timezone.now() - timedelta(days=1),
            starting_price=100000,
            current_price=100000,
            seller=self.seller
        )
        self.assertTrue(past_auction.is_expired())

class BidModelTests(TestCase):
    def setUp(self):
        # Set up similar to AuctionModelTests
        self.user1 = CustomUser.objects.create_user(username='seller1', password='test123')
        self.user2 = CustomUser.objects.create_user(username='buyer1', password='test123')
        self.seller = Seller.objects.create(user=self.user1)
        self.buyer = Buyer.objects.create(user=self.user2)
        self.house = House.objects.create(
            judul="Test House",
            lokasi="Test Location",
            deskripsi="Test Description",
            gambar="static/img/logo.png",
            kamar_tidur=2,
            kamar_mandi=1,
            harga=1000000,
            is_available=True,
            seller=self.seller
        )
        self.auction = Auction.objects.create(
            title="Test Auction",
            house=self.house,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=7),
            starting_price=100000,
            current_price=100000,
            seller=self.seller
        )

    def test_bid_str(self):
        bid = Bid.objects.create(
            auction=self.auction,
            buyer=self.buyer,
            price=150000
        )
        expected_str = f"Test Auction - buyer1 - 150000"
        self.assertEqual(str(bid), expected_str)

class AuctionFormTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='seller1', password='test123')
        self.seller = Seller.objects.create(user=self.user)
        self.house = House.objects.create(
            judul="Test House",
            lokasi="Test Location",
            deskripsi="Test Description",
            gambar="static/img/logo.png",
            kamar_tidur=2,
            kamar_mandi=1,
            harga=1000000,
            is_available=True,
            seller=self.seller
        )

    def test_valid_form(self):
        form_data = {
            'title': 'Test Auction',
            'house': self.house.id,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timedelta(days=7),
            'starting_price': 100000
        }
        form = AuctionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_dates(self):
        form_data = {
            'title': 'Test Auction',
            'house': self.house.id,
            'start_date': timezone.now(),
            'end_date': timezone.now() - timedelta(days=7),
            'starting_price': 100000
        }
        form = AuctionForm(data=form_data)
        self.assertFalse(form.is_valid())

class AuctionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create seller user
        self.seller_user = CustomUser.objects.create_user(username='seller1', password='test123')
        self.seller = Seller.objects.create(user=self.seller_user)
        # Create buyer user
        self.buyer_user = CustomUser.objects.create_user(username='buyer1', password='test123')
        self.buyer = Buyer.objects.create(user=self.buyer_user)
        # Create house
        self.house = House.objects.create(
            judul="Test House",
            lokasi="Test Location",
            deskripsi="Test Description",
            gambar="static/img/logo.png",
            kamar_tidur=2,
            kamar_mandi=1,
            harga=1000000,
            is_available=True,
            seller=self.seller
        )
        # Create auction
        self.auction = Auction.objects.create(
            title="Test Auction",
            house=self.house,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=7),
            starting_price=100000,
            current_price=100000,
            seller=self.seller
        )

    def test_index_view_requires_login(self):
        response = self.client.get(reverse('auction:index'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_index_view_with_login(self):
        self.client.login(username='seller1', password='test123')
        response = self.client.get(reverse('auction:index'))
        self.assertEqual(response.status_code, 200)

    def test_bid_view(self):
        self.client.login(username='buyer1', password='test123')
        response = self.client.post(
            reverse('auction:bid', args=[str(self.auction.id)]),
            {'price': 150000}
        )
        self.assertEqual(response.status_code, 201)
        
        # Test invalid bid (lower than current price)
        response = self.client.post(
            reverse('auction:bid', args=[str(self.auction.id)]),
            {'price': 90000}
        )
        self.assertEqual(response.status_code, 400)

    def test_create_auction_view(self):
        self.client.login(username='seller1', password='test123')
        house = House.objects.create(
            judul="Test Houses",
            lokasi="Test Location",
            deskripsi="Test Description",
            gambar="static/img/logo.png",
            kamar_tidur=2,
            kamar_mandi=1,
            harga=1000000,
            is_available=True,
            seller=self.seller
        )
        form_data = {
            'title': 'New Test Auction',
            'house': house.id,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timedelta(days=7),
            'starting_price': 100000,
            'current_price': 100000,
            'seller': self.seller.id
        }
        response = self.client.post(reverse('auction:create'), form_data)
        self.assertEqual(response.status_code, 302)  # Successful creation redirects

    def test_delete_auction_view(self):
        self.client.login(username='seller1', password='test123')
        # Create an expired auction
        expired_auction = Auction.objects.create(
            title="Expired Auction",
            house=self.house,
            start_date=timezone.now() - timedelta(days=7),
            end_date=timezone.now() - timedelta(days=1),
            starting_price=100000,
            current_price=100000,
            seller=self.seller
        )
        response = self.client.delete(
            reverse('auction:delete', args=[str(expired_auction.id)])
        )
        self.assertEqual(response.status_code, 302)  # Successful deletion redirects

    def test_get_all_auctions_view(self):
        response = self.client.get(reverse('auction:get_all_auctions'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)  # Should contain our test auction

    def test_get_auction_by_id_view(self):
        response = self.client.get(
            reverse('auction:get_auction_by_id', args=[str(self.auction.id)]),
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Test Auction')
import json
from django.core.management.base import BaseCommand
from rumah.models import House
from HouseHuntAuth.models import Seller, CustomUser
import random


class Command(BaseCommand):
    help = "Populate the database with dummy data"

    def handle(self, *args, **kwargs):

        # Read the JSON file
        with open("dataset/rumah.json") as f:
            houses = json.load(f)

        user = CustomUser.objects.create_user(
            username="seller1",
            password="test123",
            is_seller=True,
            phone_number="081234567890",
            email="test@gmail.com"
        )

        seller = Seller.objects.create(
            user=user,
            company_name="Rumah Baru",
            company_address="Jl. Raya No. 1, Jakarta",
            stars=random.uniform(0, 5),
        )

        for house in houses:
            kamar_tidur = int(house.get("kamar_tidur", 0))
            kamar_mandi = int(house.get("kamar_mandi", 0))
            housey = House.objects.create(
                seller=seller,
                harga=house["price_in_rp"],
                deskripsi=house["description"],
                judul=house["title"],
                lokasi=house["lokasi"],
                gambar="static/logo.png",
                kamar_tidur=kamar_tidur,
                kamar_mandi=kamar_mandi,
                is_available=True,
            )
            
            housey.save()
        
            

        self.stdout.write(self.style.SUCCESS("Successfully populated the database"))

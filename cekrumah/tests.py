from django.test import TestCase, Client
from django.urls import reverse
from HouseHuntAuth.models import CustomUser, Buyer, Seller
from .models import Seller, Buyer, House, Availability, Appointment
from django.utils import timezone
from django.contrib.messages import get_messages

class ViewTests(TestCase):
    def setUp(self):
        # Create users, buyer, seller, house, and availability
        self.client = Client()
        self.user_seller = CustomUser.objects.create_user(username='seller', password='sellerpass')
        self.user_buyer = CustomUser.objects.create_user(username='buyer', password='buyerpass')
        
        # Assign seller and buyer profiles
        self.seller = Seller.objects.create(user=self.user_seller)
        self.buyer = Buyer.objects.create(user=self.user_buyer)
        
        # Create a house and availability for tests
        self.house = House.objects.create(judul='Test House', is_available=True, seller=self.seller, harga=1000_000_000,
                                          kamar_tidur = 1, kamar_mandi = 1)
        self.availability = Availability.objects.create(
            seller=self.seller,
            house=self.house,
            available_date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=1)).time(),
            is_available=True
        )
    
    def test_create_availability_as_seller(self):
        self.client.login(username='seller', password='sellerpass')
        response = self.client.post(reverse('cekrumah:create_availability'), {
            'house': self.house.id,
            'available_date': timezone.now().date(),
            'start_time': '10:00',
            'end_time': '11:00',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful creation
        self.assertEqual(Availability.objects.count(), 2)  # Initial availability + new one

    def test_create_availability_as_seller_validation_error(self):
        self.client.login(username='seller', password='sellerpass')
        response = self.client.post(reverse('cekrumah:create_availability'), {})
        self.assertEqual(response.status_code, 200)

        # Check that an Availability object was NOT created, 1 from the initial availability
        self.assertEqual(Availability.objects.count(), 1)

        # Check that the form has errors (if your form requires fields)
        form = response.context['form']
        self.assertTrue(form.errors) 

    def test_create_availability_as_non_seller(self):
        self.client.login(username='buyer', password='buyerpass')
        response = self.client.post(reverse('cekrumah:create_availability'), {
            'house': self.house.id,
            'available_date': timezone.now().date(),
            'start_time': '10:00',
            'end_time': '11:00',
        })
        self.assertEqual(response.status_code, 403)  # Forbidden for non-seller
        self.assertContains(response, "You are not a seller", status_code=403)

    def test_create_appointment_as_buyer(self):
        self.client.login(username='buyer', password='buyerpass')
        response = self.client.post(reverse('cekrumah:create_appointment'), {
            'house': self.house.id,
            'availability': self.availability.id,
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful creation
        self.assertEqual(Appointment.objects.count(), 1)  # One appointment created

    def test_create_appointment_as_non_buyer(self):
        self.client.login(username='seller', password='sellerpass')
        response = self.client.post(reverse('cekrumah:create_appointment'), {
            'house': self.house.id,
            'availability': self.availability.id,
        })
        self.assertEqual(response.status_code, 403)  # Forbidden for non-buyer
        self.assertContains(response, "You are not a buyer", status_code=403)

    def test_get_availability(self):
        self.client.login(username='buyer', password='buyerpass')
        response = self.client.get(reverse('cekrumah:get_availability'), {'house_id': self.house.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['id'], self.availability.id)  # Ensure availability data is returned correctly

    def test_update_appointment_as_buyer(self):
        self.client.login(username='buyer', password='buyerpass')
        appointment = Appointment.objects.create(
            buyer=self.buyer, availability=self.availability, seller=self.seller
        )
        response = self.client.post(reverse('cekrumah:update_appointment', args=[appointment.id]), {
            'notes_to_seller': 'Updated note to seller',
            'house': appointment.availability.house.id,
            'availability': appointment.availability.id
        })
        appointment.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Should redirect after successful update
        self.assertEqual(appointment.notes_to_seller, 'Updated note to seller')

    def test_delete_appointment(self):
        self.client.login(username='buyer', password='buyerpass')
        appointment = Appointment.objects.create(
            buyer=self.buyer, availability=self.availability, seller=self.seller
        )
        response = self.client.post(reverse('cekrumah:delete_appointment', args=[appointment.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after deletion
        self.assertEqual(Appointment.objects.count(), 0)  # Appointment should be deleted

    def test_delete_availability(self):
        self.client.login(username='seller', password='sellerpass')
        response = self.client.post(reverse('cekrumah:delete_availability', args=[self.availability.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after deletion
        self.assertEqual(Availability.objects.count(), 0)  # Availability should be deleted
    
    def test_create_appointment_missing_fields_message(self):
        self.client.login(username='buyer', password='buyerpass')
        response = self.client.post(reverse('cekrumah:create_appointment'), {})
        
        # Check that the response status code is 200 (the form is shown again)
        self.assertEqual(response.status_code, 200)
        
        # Check that the message is correct
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)  # One message should be in the queue
        self.assertEqual(messages_list[0].message, "Please select a house and an available slot.")
        self.assertEqual(messages_list[0].tags, "error")  # Check if it has the 'error' tag

    def test_create_appointment_success_message(self):
        self.client.login(username='buyer', password='buyerpass')
        response = self.client.post(reverse('cekrumah:create_appointment'), {
            'house': self.house.id,
            'availability': self.availability.id,
        })

        # Check that the appointment was created
        self.assertEqual(Appointment.objects.count(), 1)

        # Check that the response redirects to the appointment list
        self.assertRedirects(response, reverse('cekrumah:appointment_list'))

        # Check that the success message was added
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)  # One message should be in the queue
        self.assertEqual(messages_list[0].message, "Appointment created successfully!")  # Success message
        self.assertEqual(messages_list[0].tags, "success")  # Check if it has the 'success' tag

    def test_update_availability_as_seller_with_messages(self):
        self.client.login(username='seller', password='sellerpass')
        availability = Availability.objects.create(
            seller=self.seller,
            house=self.house,
            available_date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=1)).time(),
            is_available=True
        )

        response = self.client.post(reverse('cekrumah:update_availability', args=[availability.id]), {
            'house': self.house.id,
            'available_date': timezone.now().date(),
            'start_time': '10:00',
            'end_time': '11:00',
            'is_available': 'False'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cekrumah:availability_list'))
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)  # One message should be in the queue
        self.assertEqual(messages_list[0].message, "Availability updated successfully!")
        self.assertEqual(messages_list[0].tags, "success")

    def test_update_availability_as_buyer(self):
        self.client.login(username='buyer', password='buyerpass')

        response = self.client.post(reverse('cekrumah:update_availability', args=[self.availability.id]), {
            'house': self.house.id,
            'available_date': timezone.now().date(),
            'start_time': '10:00',
            'end_time': '11:00',
            'is_available': 'False'
        })

        # buyer doesnt have seller attribute
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "You are not a seller", status_code=403)

    def test_update_availability_with_GET_method(self):
        self.client.login(username='seller', password='sellerpass')
        availability = Availability.objects.create(
            seller=self.seller,
            house=self.house,
            available_date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=1)).time(),
            is_available=True
        )

        response = self.client.get(reverse('cekrumah:update_availability', args=[availability.id]), {
            'house': self.house.id,
            'available_date': timezone.now().date(),
            'start_time': '10:00',
            'end_time': '11:00',
            'is_available': 'False'
        })

        # test if rendered back to the form
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('availability_form.html')
        self.assertIn('form', response.context)
    
    def test_update_appointment_status_success(self):
        # create an appointment first
        appointment = Appointment.objects.create(
            buyer=self.buyer,
            seller=self.availability.seller,
            availability=self.availability,
            notes_to_seller='Initial note'
        )

        self.client.login(username='seller', password='sellerpass')
        
        response = self.client.post(reverse('cekrumah:availability_list'), {
            'appointment_id': appointment.id,
            'status': 'approved', 
        })

        # Assert that the response is a redirect
        self.assertEqual(response.status_code, 302)  # Redirect after successful update

        # Refresh the appointment from the database
        appointment.refresh_from_db()
        
        # Assert that the appointment status has been updated
        self.assertEqual(appointment.status, 'approved') 

        # Check for success message
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(str(messages_list[0]), "Appointment status updated successfully.")

    def test_update_appointment_status_failure(self):
        appointment = Appointment.objects.create(
            buyer=self.buyer,
            seller=self.availability.seller,
            availability=self.availability,
            notes_to_seller='Initial note'
        )
        
        self.client.login(username='seller', password='sellerpass')
        response = self.client.post(reverse('cekrumah:availability_list'), {
            'appointment_id': appointment.id,
            'status': '',  # Invalid input
        })

        self.assertEqual(response.status_code, 200) 
        # Assert that the appointment status hasn't changed
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, 'pending')

        # Check for error message
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(str(messages_list[0]), "Failed to update appointment status.")

class AppointmentModelTest(TestCase):
    def setUp(self):
        # Set up the required objects
        self.user_seller = CustomUser.objects.create_user(username='seller2', password='sellerpass')
        self.user_buyer = CustomUser.objects.create_user(username='buyer2', password='buyerpass')
        self.seller = Seller.objects.create(user=self.user_seller)
        self.buyer = Buyer.objects.create(user=self.user_buyer)

        self.house = House.objects.create(judul='Test House 2', is_available=True, seller=self.seller, harga=1000_000_000,
                                          kamar_tidur = 2, kamar_mandi = 1)

        self.availability = Availability.objects.create(
            seller=self.seller,
            house=self.house,
            available_date='2024-10-30',
            start_time='10:00',
            end_time='12:00',
            is_available=True
        )
        self.appointment = Appointment.objects.create(
            buyer=self.buyer,
            seller=self.availability.seller,
            availability=self.availability,
            notes_to_seller='Initial note'
        )

    def test_appointment_str(self):
        # test for to_string of an appointment object
        self.assertEqual(str(self.appointment), 'Appointment between buyer2 and seller2 on 2024-10-30') 

    def test_appointment_notes_update(self):
        # test for updated notes
        self.appointment.notes_to_seller = 'Updated note'
        self.appointment.save()
        self.assertEqual(self.appointment.notes_to_seller, 'Updated note')
    
    def test_appointment_status(self):
        # test for default status of appointment
        self.assertEqual(self.appointment.status, 'pending')

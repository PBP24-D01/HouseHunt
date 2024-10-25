from django import forms
from cekrumah.models import Availability, Appointment
from rumah.models import House  # Import House model to filter house choices

# Form for Seller to create or manage availability
class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['house', 'available_date', 'start_time', 'end_time', 'is_available']
        widgets = {
            'available_date': forms.SelectDateWidget(),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'house': 'House',
            'available_date': 'Available Date',
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'is_available': 'Available?',
        }

    # Override the __init__ method to filter house choices by seller
    def __init__(self, *args, **kwargs):
        seller = kwargs.pop('seller', None)  # Expect seller to be passed in when the form is initialized
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        if seller:
            self.fields['house'].queryset = House.objects.filter(seller=seller)  # Limit house choices to seller's houses

# Form for Buyer to request an appointment
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['availability', 'notes_to_seller']
        widgets = {
            'notes_to_seller': forms.Textarea(attrs={'placeholder': 'Leave a note for the seller...'}),
        }
        labels = {
            'availability': 'Available Slots',
            'notes_to_seller': 'Notes to Seller (Optional)',
        }

    def clean_availability(self):
        availability = self.cleaned_data.get('availability')
        if not availability.is_available:
            raise forms.ValidationError("This slot is no longer available.")
        return availability

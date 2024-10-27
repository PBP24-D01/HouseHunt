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
            # Limit house choices to seller's houses
            houses = House.objects.filter(seller=seller)
            self.fields['house'].queryset = houses

            # Customize the labels for the house choices
            self.fields['house'].label_from_instance = lambda obj: f"{obj} (ID: {obj.id})"


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status']


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

    def __init__(self, *args, **kwargs):
        house_id = kwargs.pop('house_id', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)

        if house_id:
            # Fetch availabilities for the selected house
            availabilities = Availability.objects.filter(house_id=house_id, is_available=True)
            self.fields['availability'].queryset = availabilities
        else:
            self.fields['availability'].queryset = Availability.objects.none()  # No availabilities available if no house is selected

    def clean_availability(self):
        availability = self.cleaned_data.get('availability')
        if not availability.is_available:
            raise forms.ValidationError("This slot is no longer available.")
        return availability



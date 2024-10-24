from django.forms import ModelForm
from cekrumah.models import Appointment, Availability


class AvailabilityForm(ModelForm):
    class Meta:
        model = Availability
        fields = ["available_date", "start_time", "end_time"]

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ["status", "notes_to_seller"]
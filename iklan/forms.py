from django.forms import ModelForm
from iklan.models import IklanEntry

class IklanEntryForm(ModelForm):
    class Meta:
        model = IklanEntry
        fields = ["id_rumah", "start_date", "end_date", "banner"]
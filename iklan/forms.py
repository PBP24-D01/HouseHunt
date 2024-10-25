from django.forms import ModelForm
from iklan.models import IklanEntry

class IklanEntryForm(ModelForm):
    class Meta:
        model = IklanEntry
        fields = ["rumah", "start_date", "end_date", "banner"]
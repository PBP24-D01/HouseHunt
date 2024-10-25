from django.forms import ModelForm
from models import Review

class ReviewEntryForm(ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'rating']
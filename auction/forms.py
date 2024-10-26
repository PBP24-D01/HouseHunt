from django import forms
from .models import Auction

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'house', 'start_date', 'end_date', 'starting_price']
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be later than start date")
        return cleaned_data
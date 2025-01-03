from django.forms import ModelForm, Select
from wishlist.models import Wishlist

class WishlistForm(ModelForm):
    class Meta:
        model = Wishlist
        fields = ["notes", "priority"]
        widgets = {
            'priority': Select(choices=Wishlist.PRIORITY_CHOICES),
        }

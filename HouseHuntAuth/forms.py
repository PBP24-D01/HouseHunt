from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Buyer, Seller

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()

    def _style_fields(self):
        for field in self.fields.values():
            field.widget.attrs['class'] = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'

class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['preferred_payment_method']

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['company_name', 'company_address']

class BuyerSignUpForm(UserCreationForm):
    preferred_payment_method = forms.ChoiceField(choices=Buyer._meta.get_field('preferred_payment_method').choices)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_buyer = True
        if commit:
            user.save()
            Buyer.objects.create(
                user=user,
                preferred_payment_method=self.cleaned_data.get('preferred_payment_method')
            )
        return user

class SellerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    company_address = forms.CharField(widget=forms.Textarea)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
            Seller.objects.create(
                user=user,
                company_name=self.cleaned_data.get('company_name'),
                business_address=self.cleaned_data.get('business_address'),
                tax_id=self.cleaned_data.get('tax_id'),
                business_phone=self.cleaned_data.get('business_phone')
            )
        return user
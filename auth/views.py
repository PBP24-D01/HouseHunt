from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from .forms import (
    BuyerSignUpForm, SellerSignUpForm,
    BuyerForm, SellerForm
)
from .models import CustomUser

# Create your views here.
class RegisterBuyer(CreateView):
    model = CustomUser
    form_class = BuyerSignUpForm
    template_name = 'signup.html'
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'buyer'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Welcome! Buyer account has been created successfully.')
        return redirect('buyer_dashboard')

class RegisterSeller(CreateView):
    model = CustomUser
    form_class = SellerSignUpForm
    template_name = 'signup.html'
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'seller'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Welcome! Seller account has been created successfully.')
        return redirect('seller_dashboard')
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView
from .forms import BuyerSignUpForm, SellerSignUpForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
class RegisterBuyer(CreateView):
    model = CustomUser
    form_class = BuyerSignUpForm
    template_name = "register.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "buyer"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request, "Welcome to HouseHunt as Buyer!"
        )
        return redirect("/")


class RegisterSeller(CreateView):
    model = CustomUser
    form_class = SellerSignUpForm
    template_name = "register.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "seller"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request, "Welcome to Househunt as Seller!"
        )
        return redirect("/")

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}.")
            return redirect("/")
    else:
        form = AuthenticationForm(request)
    context = {"form": form}
    return render(request, "login.html", context)

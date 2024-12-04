import datetime
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from .forms import BuyerSignUpForm, SellerSignUpForm
from .models import CustomUser, Seller, Buyer
from django.contrib.auth.forms import AuthenticationForm


def profile(request):
    user = request.user
    context = {
        "user": user,
    }
    return render(request, "profile.html", context)


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
        messages.success(self.request, "Welcome to HouseHunt as Buyer!")
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
        messages.success(self.request, "Welcome to Househunt as Seller!")
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


@csrf_exempt
def login_api(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse(
                {
                    "id": user.id,
                    "username": user.username,
                    "status": True,
                    "message": "Login sukses!",
                    # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
                },
                status=200,
            )
        else:
            return JsonResponse(
                {"status": False, "message": "Login gagal, akun dinonaktifkan."},
                status=401,
            )

    else:
        return JsonResponse(
            {
                "status": False,
                "message": "Login gagal, periksa kembali email atau kata sandi.",
            },
            status=401,
        )


@csrf_exempt
def register_seller(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data["username"]
        email = data["email"]
        phone_number = data["phone_number"]
        company_name = data["company_name"]
        company_address = data["company_address"]
        password1 = data["password1"]
        password2 = data["password2"]
        
        # Check missing fields
        if not username or not email or not phone_number or not company_name or not company_address or not password1 or not password2:
            return JsonResponse(
                {"status": False, "message": "All fields are required."}, status=400
            )

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse(
                {"status": False, "message": "Passwords do not match."}, status=400
            )

        # Check if the username is already taken
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse(
                {"status": False, "message": "Username already exists."}, status=400
            )

        # Check if the email is already taken
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse(
                {"status": False, "message": "Email already exists."}, status=400
            )

        # Check if the phone number is already taken
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return JsonResponse(
                {"status": False, "message": "Phone number already exists."}, status=400
            )

        try:
            # Create the new user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                phone_number=phone_number,
                is_buyer=False,
                is_seller=True,
                password=password1,
            )
            user.save()

            # Create the seller
            seller = Seller.objects.create(
                user=user,
                company_name=company_name,
                company_address=company_address,
            )
            seller.save()
        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=400)

        return JsonResponse(
            {
                "username": username,
                "status": "success",
                "message": "User created successfully!",
            },
            status=200,
        )

    else:
        return JsonResponse(
            {"status": False, "message": "Invalid request method."}, status=400
        )


@csrf_exempt
def register_buyer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data["username"]
        email = data["email"]
        phone_number = data["phone_number"]
        preffered_payment_method = data["preffered_payment_method"]
        password1 = data["password1"]
        password2 = data["password2"]
        
        # Check missing fields
        if not username or not email or not phone_number or not preffered_payment_method or not password1 or not password2:
            return JsonResponse(
                {"status": False, "message": "All fields are required."}, status=400
            )

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse(
                {"status": False, "message": "Passwords do not match."}, status=400
            )

        # Check if the username is already taken
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse(
                {"status": False, "message": "Username already exists."}, status=400
            )

        # Check if the email is already taken
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse(
                {"status": False, "message": "Email already exists."}, status=400
            )

        # Check if the phone number is already taken
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return JsonResponse(
                {"status": False, "message": "Phone number already exists."}, status=400
            )

        try:
            # Create the new user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                phone_number=phone_number,
                is_buyer=False,
                is_seller=True,
                password=password1,
            )
            user.save()

            # Create the buyer
            buyer = Buyer.objects.create(
                user=user,
                preferred_payment_method=preffered_payment_method,
            )
            buyer.save()
        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=400)

        return JsonResponse(
            {
                "username": username,
                "status": "success",
                "message": "User created successfully!",
            },
            status=200,
        )

    else:
        return JsonResponse(
            {"status": False, "message": "Invalid request method."}, status=400
        )


@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse(
            {"username": username, "status": True, "message": "Logout berhasil!"},
            status=200,
        )
    except:
        return JsonResponse({"status": False, "message": "Logout gagal."}, status=401)

def get_user(request):
    user = request.user
    if user.is_authenticated:
        if user.is_buyer:
            buyer = Buyer.objects.get(user=user)
            return JsonResponse(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "is_buyer": True,
                    "preferred_payment_method": buyer.preferred_payment_method,
                },
                status=200,
            )
        else:
            seller = Seller.objects.get(user=user)
            return JsonResponse(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "is_buyer": False,
                    "company_name": seller.company_name,
                    "company_address": seller.company_address,
                },
                status=200,
            )
    else:
        return JsonResponse(
            {"status": False, "message": "User is not authenticated."}, status=401
        )
from django.shortcuts import render
from cekrumah.forms import AvailabilityForm

# Create your views here.
def make_appointment(request):
    pass


def show_appointments(request):
    pass


def add_available_dates(request):
    form = AvailabilityForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        form.save()

    context = {'form':form}
    return render(request, 'add_available_dates.html', context)

def delete_appointment(request):
    pass


def change_status(request):
    pass

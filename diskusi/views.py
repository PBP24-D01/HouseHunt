from django.shortcuts import render
# from .forms import ReviewEntryForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

#@login_required(login_url='/login')
def main_page(request):
    return render(request, 'list_penjual.html')
# def review(request):
#     if request.method == 'POST':
#         form = ReviewEntryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('review')
        
#     return render(request, 'review.html', {'form': form})
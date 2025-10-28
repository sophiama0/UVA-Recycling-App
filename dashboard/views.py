from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import RecyclingBin


# Create your views here.
def index(request):
    return render(request, "dashboard/index.html")

@login_required
def profile(request):
    return render(request, "dashboard/profile.html")

@login_required
def home_view(request):
    bins = RecyclingBin.objects.all().order_by('-last_updated')
    return render(request, 'main/index.html', {'bins': bins})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "dashboard/index.html")

@login_required
def profile(request):
    return render(request, "dashboard/profile.html")
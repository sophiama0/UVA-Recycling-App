from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    profile = getattr(request.user, 'profile', None)

    if profile and profile.user_type == 'admin':
        return render(request, 'admin_dashboard.html')
    else:
        return render(request, 'regular_dashboard.html')

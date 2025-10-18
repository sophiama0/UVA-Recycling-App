from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    profile = getattr(request.user, 'profile', None)
    print(request.user.profile.user_type)

    if profile and profile.user_type == 'admin':
        return render(request, 'main/admin_dashboard.html')
    else:
        return render(request, 'main/regular_dashboard.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from recycling_spots.models import RecyclingSpot # Import your new model

@login_required
def index(request):
    """
    View function for the main dashboard page.
    """
    posted_bins_count = RecyclingSpot.objects.filter(author=request.user).count()
    
    context = {
        'display_name': request.user.first_name or request.user.username,
        'posted_bins_count': posted_bins_count,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def profile(request):
    """
    This is the original profile URL. We redirect it to the new one.
    """
    return redirect('dashboard:profile')

@login_required
def inbox(request):
    """
    Placeholder view for the inbox.
    """
    # Add logic for your inbox here
    return render(request, 'dashboard/index.html') # Placeholder template

@login_required
def chat(request, username):
    """
    Placeholder view for the chat.
    """
    # Add logic for your chat here
    context = {'chat_with_username': username}
    return render(request, 'dashboard/index.html', context) # Placeholder template

@login_required
def profile_view(request):
    """
    View function for the new profile page.
    """
    posted_bins_count = RecyclingSpot.objects.filter(author=request.user).count()

    times_recycled = "N/A"
    bins_used = "N/A"
    most_used = "N/A"

    context = {
        'posted_bins_count': posted_bins_count,
        'times_recycled': times_recycled,
        'bins_used': bins_used,
        'most_used': most_used,
        'display_name': request.user.first_name or request.user.username,
    }
    return render(request, 'dashboard/profile.html', context)
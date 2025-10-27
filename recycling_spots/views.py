from django.shortcuts import render, redirect # Add redirect
from django.contrib.auth.decorators import login_required
from .models import RecyclingSpot # Import the model
from .forms import RecyclingSpotForm # Import the form

# Updated view to show the list of spots from the database
def spot_list_view(request):
    # Query all RecyclingSpot objects from the database, order by newest first
    all_spots = RecyclingSpot.objects.all().order_by('-created_at')
    # Pass the spots to the template context
    context = {'spots': all_spots}
    return render(request, 'recycling_spots/spot_list.html', context)

# Updated view to handle form submission (POST) and display (GET)
@login_required
def create_spot_view(request):
    if request.method == 'POST':
        # Data is being submitted
        form = RecyclingSpotForm(request.POST)
        if form.is_valid():
            # Form data is valid, create a model instance but don't save yet
            spot = form.save(commit=False)
            # Assign the currently logged-in user as the author
            spot.author = request.user
            # Now save the complete object to the database
            spot.save()
            # Redirect the user back to the list page after saving
            return redirect('spot_list')
        else:
            # Form is invalid, re-render the page with the form and errors
            pass # Fall through to render below
    else:
        # Request method is GET, just show a blank form
        form = RecyclingSpotForm()

    # Pass the form (either blank or with errors) to the template
    context = {'form': form}
    return render(request, 'recycling_spots/create_spot.html', context)
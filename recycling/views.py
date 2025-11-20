from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from django.shortcuts import render

from .forms import ProfileImageForm, RecyclingBinForm, RecyclingBinUpdateForm, UserNameForm, RecyclingFullnessForm, ProfileBioForm, ProfileSustainabilityInterests
from .models import RecyclingBin, BinVote, BinUsage


# Create your views here.
def map_page(request):
    return render(request, "recycling/map.html")

def bin_locations(request):
    bins = RecyclingBin.objects.all()
    data = [
        {
            "id": b.id,
            "name": b.name,
            "description": b.description,
            "latitude": float(b.latitude),
            "longitude": float(b.longitude),
        }
        for b in bins
    ]
    return JsonResponse(data, safe=False)



def recycling_map(request):
    bins = RecyclingBin.objects.all().order_by('-created_at')

    user_votes = {}
    if request.user.is_authenticated:
        votes = BinVote.objects.filter(user=request.user)
        user_votes = {vote.recycling_bin_id: vote.vote_type for vote in votes}

    for bin in bins:
        bin.user_vote = user_votes.get(bin.id)

    context = {
        'bins': bins,
        'recycling_map_active': 'active',
    }
    return render(request, 'recycling/recycling-map.html', context)



class RecyclingBinDetailView(DetailView):
    model = RecyclingBin
    template_name = 'recycling/recycling-bin-detail.html'
    context_object_name = 'bin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        bin = self.get_object()
        if user.is_authenticated:
            context['user_vote'] = bin.get_user_vote(user)
            context['user_recycle_count'] = BinUsage.get_user_bin_usage_count(user, bin)
        else:
            context['user_vote'] = None
        return context


def vote_bin(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to upvote or downvote a recycling location.")
        return redirect('recycling-bin-detail', pk=pk)

    bin = get_object_or_404(RecyclingBin, pk=pk)
    vote_type = request.POST.get('vote_type')

    vote, created = BinVote.objects.get_or_create(user=request.user, recycling_bin=bin)
    if not created and vote.vote_type == vote_type:
        vote.delete()
    else:
        vote.vote_type = vote_type
        vote.save()

    return redirect('recycling-bin-detail', pk=pk)


def community(request):
    users = User.objects.exclude(id=request.user.id)
    context = {
        'other_users': users,
        'community_active': 'active'
    }

    return render(request, 'recycling/community.html', context)


@login_required
def recycle_here(request, pk):
    """Record that the current user recycled at bin `pk` and redirect back to the detail page."""
    if request.method != 'POST':
        return redirect('recycling-bin-detail', pk=pk)

    bin = get_object_or_404(RecyclingBin, pk=pk)

    BinUsage.objects.create(user=request.user, recycling_bin=bin)

    messages.success(request, f"Thank you for recycling at {bin.name}!")

    return redirect('recycling-bin-detail', pk=pk)



@login_required
def update_fullness_after_recycle(request, pk):
    """Show a form to update the bin fullness after the user indicates they recycled here.

    On GET: create a BinUsage record (the user just recycled) and show the form with current value.
    On POST: validate and save the fullness (as percent -> decimal 0..1), set updated_by, and redirect to recycling-map.
    """
    bin = get_object_or_404(RecyclingBin, pk=pk)

    if request.method == 'POST':
        form = RecyclingFullnessForm(request.POST)
        if form.is_valid():
            pct = form.cleaned_data['fullness_percent']
            # convert percent to 0..1 decimal
            bin.fullness = round((pct / 100), 2)
            bin.updated_by = request.user
            bin.save()
            messages.success(request, f"Fullness updated for {bin.name}.")
            return redirect('recycling-map')
    else:
        # create a BinUsage record when the user arrives here (they indicated they recycled)
        BinUsage.objects.create(user=request.user, recycling_bin=bin)
        initial_pct = bin.fullness * 100
        form = RecyclingFullnessForm(initial={'fullness_percent': initial_pct})

    return render(request, 'recycling/update-fullness.html', {'form': form, 'bin': bin})



@login_required
def delete_bin_confirm(request, pk):
    """Confirm and delete a RecyclingBin. Only allowed for staff, superusers, or the user who posted the bin."""
    bin = get_object_or_404(RecyclingBin, pk=pk)

    user = request.user
    allowed = user.is_authenticated and (user.is_staff or user.is_superuser or bin.posted_by == user)
    if not allowed:
        messages.error(request, "You do not have permission to delete this bin.")
        return redirect('recycling-bin-detail', pk=pk)

    if request.method == 'POST':
        # delete the bin (related votes/usages are cascade-deleted)
        bin_name = bin.name
        bin.delete()
        messages.success(request, f"{bin_name} has been deleted.")
        return redirect('recycling-map')

    # GET: show confirmation page
    return render(request, 'recycling/delete-confirm.html', {'bin': bin})


def post_recycling_location(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to post a recycling location.")
        return redirect('recycling-map')

    if request.method == 'POST':
        form = RecyclingBinForm(request.POST, request.FILES)
        if form.is_valid():
            bin = form.save(commit=False)
            bin.posted_by = request.user
            bin.updated_by = request.user
            bin.save()
            return redirect('recycling-map')
    else:
        form = RecyclingBinForm()

    return render(request, 'recycling/post-recycling-location.html', {'form': form})


@login_required
def update_recycling_location(request, pk):
    bin = get_object_or_404(RecyclingBin, pk=pk)

    if request.method == 'POST':
        form = RecyclingBinUpdateForm(request.POST, request.FILES, instance=bin, user=request.user)
        if form.is_valid():
            updated_bin = form.save(commit=False)
            updated_bin.updated_by = request.user
            updated_bin.save()
            return redirect('recycling-bin-detail', pk=bin.pk)
    else:
        form = RecyclingBinUpdateForm(instance=bin, user=request.user)

    return render(request, 'recycling/update-recycling-location.html', {'form': form, 'bin': bin})


@login_required
def profile(request, first_name, user_id):
    user_obj = get_object_or_404(User, id=user_id, first_name=first_name)

    context = {
        'profile_user': user_obj,
        'profile_active': 'active'
        }

    return render(request, "recycling/profile.html", context)


@login_required
def settings(request):
    profile = request.user.profile
    user = request.user

    if request.method == 'POST':
        if 'update_name' in request.POST:
            name_form = UserNameForm(request.POST, instance=user)
            if name_form.is_valid():
                name_form.save()
                return redirect('settings')
            image_form = ProfileImageForm(instance=profile)
        elif 'update_image' in request.POST:
            image_form = ProfileImageForm(request.POST, request.FILES, instance=profile)
            if image_form.is_valid():
                image_form.save()
                return redirect('settings')
            name_form = UserNameForm(instance=user)
        elif 'update_bio' in request.POST:
            bio_form = ProfileBioForm(request.POST, instance=profile)
            if bio_form.is_valid():
                bio_form.save()
                return redirect('settings')
        elif 'update_sustainability_interests' in request.POST:
            sustainability_form = ProfileSustainabilityInterests(request.POST, instance=profile)
            if sustainability_form.is_valid():
                sustainability_form.save()
                return redirect('settings')
    else:
        name_form = UserNameForm(instance=user)
        image_form = ProfileImageForm(instance=profile)
        bio_form = ProfileBioForm(instance=profile)
        sustainability_form = ProfileSustainabilityInterests(instance=profile)

    context = {
        'name_form': name_form,
        'image_form': image_form,
        'bio_form': bio_form,
        'sustainability_form': sustainability_form,
    }
    return render(request, 'recycling/settings.html', context)
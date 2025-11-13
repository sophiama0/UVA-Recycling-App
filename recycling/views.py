from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.detail import DetailView

from .forms import ProfileImageForm, RecyclingBinForm, RecyclingBinUpdateForm, UserNameForm, RecyclingFullnessForm
from .models import RecyclingBin, BinVote, BinUsage


# Create your views here.
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
def profile(request):
    return render(request, "recycling/profile.html", {'profile_active': 'active'})


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
    else:
        name_form = UserNameForm(instance=user)
        image_form = ProfileImageForm(instance=profile)

    context = {
        'name_form': name_form,
        'image_form': image_form,
    }
    return render(request, 'recycling/settings.html', context)
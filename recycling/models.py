from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Count


# Create your models here.
class RecyclingBin(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    fullness = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0),MaxValueValidator(1)], default=0.0)
    image = models.ImageField(upload_to='recycling_bin_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_bins')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_bins')

    def __str__(self):
        return self.name
    
    @property
    def fullness_percentage(self):
        return self.fullness * 100
    
    @property
    def upvote_count(self):
        return self.votes.filter(vote_type='up').count()

    @property
    def downvote_count(self):
        return self.votes.filter(vote_type='down').count()

    def get_user_vote(self, user):
        """Return 'up', 'down', or None depending on what this user voted."""
        if not user.is_authenticated:
            return None
        vote = self.votes.filter(user=user).first()
        return vote.vote_type if vote else None



class BinVote(models.Model):
    VOTE_CHOICES = [
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bin_votes')
    recycling_bin = models.ForeignKey(RecyclingBin, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=5, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recycling_bin')  # each user can only have one vote per bin

    def __str__(self):
        return f"{self.user.username} {self.vote_type}d {self.recycling_bin.name}"


class BinUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bin_usage')
    recycling_bin = models.ForeignKey(RecyclingBin, on_delete=models.CASCADE, related_name='usage_records')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    @classmethod
    def get_user_bin_usage_count(cls, user, recycling_bin):
        return cls.objects.filter(user=user, recycling_bin=recycling_bin).count()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    bio = models.TextField(blank=True, default = "")

    @property
    def total_bins_used(self):
        return self.user.bin_usage.values('recycling_bin').distinct().count()

    @property
    def total_usage_count(self):
        return self.user.bin_usage.count()
        
    @property
    def most_used_bin_id(self):
        most_used = self.user.bin_usage.values('recycling_bin').annotate(
            usage_count=Count('recycling_bin')
        ).order_by('-usage_count').first()
        return most_used['recycling_bin'] if most_used else None

    @property
    def posted_bins_count(self):
        return self.user.posted_bins.count()

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_most_used_bin_name(self):
        if self.most_used_bin_id:
            bin_obj = RecyclingBin.objects.filter(id=self.most_used_bin_id).first()
            return bin_obj.name if bin_obj else None
        return None

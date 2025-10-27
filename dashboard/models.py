from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class RecyclingBin(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_full = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_bins')
    last_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_bins')
    image_url = models.URLField(max_length=500, blank=True, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture_url = models.URLField(max_length=500, blank=True, null=True)

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

class BinUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bin_usage')
    recycling_bin = models.ForeignKey(RecyclingBin, on_delete=models.CASCADE, related_name='usage_records')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    @classmethod
    def get_user_bin_usage_count(cls, user, recycling_bin):
        return cls.objects.filter(user=user, recycling_bin=recycling_bin).count()
    
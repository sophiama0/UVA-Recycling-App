from django.contrib import admin
from .models import RecyclingBin, BinUsage, UserProfile

# Registered models
admin.site.register(RecyclingBin)
admin.site.register(BinUsage)
admin.site.register(UserProfile)
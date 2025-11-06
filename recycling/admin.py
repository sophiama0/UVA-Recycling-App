from django.contrib import admin
from .models import RecyclingBin, BinUsage, UserProfile

# Register your models here.
admin.site.register(RecyclingBin)
admin.site.register(BinUsage)
admin.site.register(UserProfile)
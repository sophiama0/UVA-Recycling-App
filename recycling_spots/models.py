from django.db import models
from django.conf import settings 

class RecyclingSpot(models.Model):
    # Link to the user who posted the spot 
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # Information about the spot
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return self.title

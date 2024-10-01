from django.db import models
from django.conf import settings

class CollectedImage(models.Model):
    original_image = models.ImageField(upload_to='original_images/')
    anonymized_image = models.ImageField(upload_to='anonymized_images/', null=True, blank=True)
    collected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    collected_at = models.DateTimeField(auto_now_add=True)
    anonymized_at = models.DateTimeField(null=True, blank=True)
    sent_to_central = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Collected Image {self.id} - Anonymized: {'Yes' if self.anonymized_image else 'No'}"

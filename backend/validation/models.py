from django.db import models
from django.conf import settings

class ImageValidation(models.Model):
    image = models.ImageField(upload_to='raw_images/')
    is_valid = models.BooleanField(default=False)
    validation_message = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Validation {self.id} - Valid: {self.is_valid}"

from django.db import models
from django.conf import settings

class ImageClassification(models.Model):
    image = models.ImageField(upload_to='processed_images/')
    classification_result = models.JSONField()
    confidence_score = models.FloatField()
    classified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Classification {self.id} - Confidence: {self.confidence_score}"

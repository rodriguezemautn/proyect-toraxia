from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CollectedImage
from .serializers import CollectedImageSerializer
from .services import anonymize_image, send_to_central_server
from django.utils import timezone

class CollectedImageViewSet(viewsets.ModelViewSet):
    queryset = CollectedImage.objects.all()
    serializer_class = CollectedImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(collected_by=self.request.user)

    @action(detail=True, methods=['POST'])
    def anonymize(self, request, pk=None):
        collected_image = self.get_object()
        anonymized = anonymize_image(collected_image.original_image)
        collected_image.anonymized_image = anonymized
        collected_image.anonymized_at = timezone.now()
        collected_image.save()
        return Response({'status': 'image anonymized'})

    @action(detail=True, methods=['POST'])
    def send_to_central(self, request, pk=None):
        collected_image = self.get_object()
        if not collected_image.anonymized_image:
            return Response({'error': 'Image must be anonymized before sending'}, status=status.HTTP_400_BAD_REQUEST)
        
        success = send_to_central_server(collected_image.anonymized_image)
        if success:
            collected_image.sent_to_central = True
            collected_image.sent_at = timezone.now()
            collected_image.save()
            return Response({'status': 'image sent to central server'})
        else:
            return Response({'error': 'Failed to send image to central server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

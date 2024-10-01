from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ImageValidation
from .serializers import ImageValidationSerializer
from .services import validate_image

class ImageValidationViewSet(viewsets.ModelViewSet):
    queryset = ImageValidation.objects.all()
    serializer_class = ImageValidationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def validate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['image']
        
        is_valid, message = validate_image(image)
        
        validation = ImageValidation.objects.create(
            image=image,
            is_valid=is_valid,
            validation_message=message,
            uploaded_by=request.user
        )
        
        return Response({
            'id': validation.id,
            'is_valid': is_valid,
            'message': message
        }, status=status.HTTP_200_OK)

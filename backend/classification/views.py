from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ImageClassification
from .serializers import ImageClassificationSerializer
from .services import classify_image

class ImageClassificationViewSet(viewsets.ModelViewSet):
    queryset = ImageClassification.objects.all()
    serializer_class = ImageClassificationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def classify(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['image']
        
        classification_result, confidence_score = classify_image(image)
        
        classification = ImageClassification.objects.create(
            image=image,
            classification_result=classification_result,
            confidence_score=confidence_score,
            classified_by=request.user
        )
        
        return Response({
            'id': classification.id,
            'classification_result': classification_result,
            'confidence_score': confidence_score
        }, status=status.HTTP_200_OK)

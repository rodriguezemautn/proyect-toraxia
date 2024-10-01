# settings.py
INSTALLED_APPS += [
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}

# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Paciente, Estudio
from .serializers import PacienteSerializer, EstudioSerializer
import logging

logger = logging.getLogger(__name__)

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        logger.info(f"Usuario {request.user} solicitó lista de pacientes")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Usuario {request.user} accedió a los datos del paciente {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def importar_hl7(self, request):
        # Lógica para importar datos de pacientes desde un mensaje HL7
        # Este es un ejemplo simplificado
        hl7_data = request.data.get('hl7_message')
        try:
            # Procesar hl7_data y crear/actualizar paciente
            paciente = Paciente.objects.create(
                nombre=hl7_data['nombre'],
                apellido=hl7_data['apellido'],
                fecha_nacimiento=hl7_data['fecha_nacimiento'],
                dni=hl7_data['dni']
            )
            logger.info(f"Paciente importado desde HL7: {paciente.id}")
            return Response({'status': 'Paciente importado correctamente'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error al importar paciente desde HL7: {str(e)}")
            return Response({'error': 'Error al procesar el mensaje HL7'}, status=status.HTTP_400_BAD_REQUEST)

class EstudioViewSet(viewsets.ModelViewSet):
    queryset = Estudio.objects.all()
    serializer_class = EstudioSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        estudio = serializer.save(medico_solicitante=self.request.user)
        logger.info(f"Estudio creado: {estudio.id} por el usuario {self.request.user}")

    @action(detail=True, methods=['post'])
    def solicitar_clasificacion(self, request, pk=None):
        estudio = self.get_object()
        # Aquí iría la lógica para enviar la imagen al servicio de ML
        # Por ahora, solo simularemos el proceso
        estudio.estado = 'EN_PROCESO'
        estudio.save()
        logger.info(f"Clasificación solicitada para el estudio {estudio.id}")
        return Response({'status': 'Clasificación solicitada'}, status=status.HTTP_202_ACCEPTED)

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import PacienteViewSet, EstudioViewSet

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)
router.register(r'estudios', EstudioViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="API de Gestión de Pacientes y Estudios",
      default_version='v1',
      description="API para el sistema de detección de anomalías en RX",
   ),
   public=True,
)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

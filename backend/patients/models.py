# models.py
from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

class Estudio(models.Model):
    TIPO_CHOICES = [
        ('RX', 'Radiografía'),
        ('TC', 'Tomografía Computarizada'),
        ('RM', 'Resonancia Magnética'),
    ]
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='estudios')
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    fecha_realizado = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    imagen_url = models.URLField()
    resultado = models.TextField(blank=True, null=True)
    medico_solicitante = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='estudios_solicitados')
    tecnico_realizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='estudios_realizados')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo} - {self.paciente} - {self.fecha_realizado}"

# serializers.py
from rest_framework import serializers
from .models import Paciente, Estudio

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class EstudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudio
        fields = '__all__'

# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Paciente, Estudio
from .serializers import PacienteSerializer, EstudioSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]

class EstudioViewSet(viewsets.ModelViewSet):
    queryset = Estudio.objects.all()
    serializer_class = EstudioSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(medico_solicitante=self.request.user)

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PacienteViewSet, EstudioViewSet

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)
router.register(r'estudios', EstudioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

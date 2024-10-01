from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Patient, Study, Appointment
from .serializers import UserSerializer, PatientSerializer, StudySerializer, AppointmentSerializer
from .permissions import IsAdminUser, IsMedicalStaff

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsMedicalStaff]

class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    permission_classes = [permissions.IsAuthenticated, IsMedicalStaff]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsMedicalStaff]

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def stats(self, request):
        patient_count = Patient.objects.count()
        study_count = Study.objects.count()
        appointment_count = Appointment.objects.count()
        return Response({
            'patient_count': patient_count,
            'study_count': study_count,
            'appointment_count': appointment_count
        })

    @action(detail=False, methods=['get'])
    def recent_activity(self, request):
        # Implementar lógica para obtener actividad reciente
        return Response([])

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PatientViewSet, StudyViewSet, AppointmentViewSet, DashboardViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'studies', StudyViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

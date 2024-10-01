from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Patient

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password123')
        self.client.force_authenticate(user=self.admin_user)

    def test_create_user(self):
        url = reverse('user-list')
        data = {'username': 'testuser', 'email': 'test@test.com', 'password': 'testpass123', 'role': 'MEDIC'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

class PatientTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.medic_user = User.objects.create_user('medic', 'medic@test.com', 'password123', role='MEDIC')
        self.client.force_authenticate(user=self.medic_user)

    def test_create_patient(self):
        url = reverse('patient-list')
        data = {'name': 'John Doe', 'date_of_birth': '1990-01-01', 'gender': 'M'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)

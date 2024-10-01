from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('MEDIC', 'Médico'),
        ('TECH', 'Técnico RX'),
        ('EMPLOYEE', 'Empleado Administrativo'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    ldap_dn = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

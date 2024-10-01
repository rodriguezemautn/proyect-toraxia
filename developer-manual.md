# Manual del Desarrollador - Core Hospitalario

## Índice
1. [Estructura del Proyecto](#1-estructura-del-proyecto)
2. [Configuración del Entorno](#2-configuración-del-entorno)
3. [Backend (Django)](#3-backend-django)
   - [Modelos](#31-modelos)
   - [Vistas](#32-vistas)
   - [Serializers](#33-serializers)
   - [URLs y Endpoints](#34-urls-y-endpoints)
4. [Frontend (React)](#4-frontend-react)
   - [Componentes](#41-componentes)
   - [Hooks Personalizados](#42-hooks-personalizados)
   - [Servicios](#43-servicios)
5. [API Reference](#5-api-reference)
6. [Flujos de Trabajo](#6-flujos-de-trabajo)
7. [Despliegue](#7-despliegue)
8. [Troubleshooting](#8-troubleshooting)

## 1. Estructura del Proyecto

```
core-hospitalario/
├── backend/
│   ├── classification/
│   ├── core/
│   ├── patients/
│   ├── studies/
│   ├── tests/
│   ├── users/
│   ├── validation/
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── Dockerfile
│   └── package.json
├── docs/
├── docker-compose.yml
└── README.md
```

## 2. Configuración del Entorno

### Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
DB_NAME=core_hospitalario
DB_USER=user
DB_PASSWORD=password
DB_HOST=db
DB_PORT=5432
```

## 3. Backend (Django)

### 3.1 Modelos

#### users/models.py
```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('DOCTOR', 'Médico'),
        ('TECH', 'Técnico RX'),
        ('STAFF', 'Personal Administrativo'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
```

#### patients/models.py
```python
from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
```

### 3.2 Vistas

#### patients/views.py
```python
from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
```

### 3.3 Serializers

#### patients/serializers.py
```python
from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
```

### 3.4 URLs y Endpoints

#### core/urls.py
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from patients.views import PatientViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

## 4. Frontend (React)

### 4.1 Componentes

#### src/components/PatientList.tsx
```typescript
import React, { useState, useEffect } from 'react';
import { getPatients } from '../services/api';

const PatientList: React.FC = () => {
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    const fetchPatients = async () => {
      const data = await getPatients();
      setPatients(data);
    };
    fetchPatients();
  }, []);

  return (
    <ul>
      {patients.map(patient => (
        <li key={patient.id}>{patient.name}</li>
      ))}
    </ul>
  );
};

export default PatientList;
```

### 4.2 Hooks Personalizados

#### src/hooks/useAuth.ts
```typescript
import { useState, useEffect } from 'react';
import { login, logout } from '../services/api';

export const useAuth = () => {
  const [user, setUser] = useState(null);

  const loginUser = async (username, password) => {
    const userData = await login(username, password);
    setUser(userData);
  };

  const logoutUser = () => {
    logout();
    setUser(null);
  };

  return { user, loginUser, logoutUser };
};
```

### 4.3 Servicios

#### src/services/api.ts
```typescript
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export const getPatients = async () => {
  const response = await axios.get(`${API_URL}/patients/`);
  return response.data;
};

export const login = async (username, password) => {
  const response = await axios.post(`${API_URL}/auth/login/`, { username, password });
  return response.data;
};

export const logout = () => {
  // Implementar lógica de logout
};
```

## 5. API Reference

### Patients

- `GET /api/patients/`: Lista todos los pacientes
- `POST /api/patients/`: Crea un nuevo paciente
- `GET /api/patients/{id}/`: Obtiene detalles de un paciente específico
- `PUT /api/patients/{id}/`: Actualiza un paciente
- `DELETE /api/patients/{id}/`: Elimina un paciente

### Authentication

- `POST /api/auth/login/`: Inicia sesión de usuario
- `POST /api/auth/logout/`: Cierra sesión de usuario

## 6. Flujos de Trabajo

### Proceso de Clasificación de Imágenes
1. El técnico de RX carga una imagen radiográfica.
2. El sistema valida que la imagen sea una radiografía válida.
3. Se aplica el modelo de IA para clasificar la imagen.
4. Los resultados se almacenan y se notifica al médico.

## 7. Despliegue

### Usando Docker
1. Asegúrate de tener Docker y Docker Compose instalados.
2. Ejecuta `docker-compose up --build` en la raíz del proyecto.
3. Accede a la aplicación en `http://localhost:3000`.

### Despliegue Manual
1. Configura un servidor web (por ejemplo, Nginx) para servir el frontend.
2. Configura Gunicorn para el backend Django.
3. Configura una base de datos PostgreSQL.
4. Asegúrate de que todas las variables de entorno estén configuradas correctamente.

## 8. Troubleshooting

### Problema: El backend no se conecta a la base de datos
- Verifica las credenciales en el archivo `.env`.
- Asegúrate de que el servicio de PostgreSQL esté en ejecución.

### Problema: CORS errors en el frontend
- Verifica que `CORS_ALLOWED_ORIGINS` en el backend incluya la URL del frontend.
- Asegúrate de que las peticiones del frontend incluyan las credenciales (withCredentials: true).

### Problema: Las imágenes no se clasifican correctamente
- Verifica que el modelo de IA esté cargado correctamente.
- Asegúrate de que las imágenes cumplan con los requisitos de formato y tamaño.

Para más información o soporte, contacta al equipo de desarrollo en support@corehospitalario.com.

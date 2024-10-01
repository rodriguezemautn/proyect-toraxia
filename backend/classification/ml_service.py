# requirements.txt
Django==5.0.1
djangorestframework==3.14.0
tensorflow==2.15.0
Pillow==10.2.0
numpy==1.26.3
gunicorn==21.2.0

# settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'

DEBUG = False

ALLOWED_HOSTS = ['*']  # Ajustar según el entorno de producción

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'ml_classifier',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ml_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ml_service.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ml_classifier/models.py
from django.db import models

class ClassificationResult(models.Model):
    image_id = models.CharField(max_length=100, unique=True)
    prediction = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Classification for {self.image_id}"

# ml_classifier/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ClassificationResult
import tensorflow as tf
from tensorflow.keras.applications.densenet import DenseNet121, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
import io

class ClassifierView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = self.load_model()

    def load_model(self):
        base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
        output = tf.keras.layers.Dense(1, activation='sigmoid')(x)
        model = tf.keras.Model(inputs=base_model.input, outputs=output)
        model.load_weights('path_to_your_trained_weights.h5')
        return model

    def preprocess_image(self, image):
        img = Image.open(io.BytesIO(image)).convert('RGB')
        img = img.resize((224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return preprocess_input(img_array)

    def post(self, request):
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        image = request.FILES['image'].read()
        processed_image = self.preprocess_image(image)
        prediction = self.model.predict(processed_image)

        result = ClassificationResult.objects.create(
            image_id=request.FILES['image'].name,
            prediction={'anomaly_probability': float(prediction[0][0])}
        )

        return Response({
            'image_id': result.image_id,
            'prediction': result.prediction
        }, status=status.HTTP_200_OK)

# ml_classifier/urls.py
from django.urls import path
from .views import ClassifierView

urlpatterns = [
    path('classify/', ClassifierView.as_view(), name='classify'),
]

# ml_service/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ml_classifier.urls')),
]

# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "ml_service.wsgi:application", "--bind", "0.0.0.0:8000"]

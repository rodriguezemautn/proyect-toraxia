# Diseño Detallado del Servicio de Clasificación de Imágenes

## 1. Visión General

El Servicio de Clasificación de Imágenes es responsable de analizar las radiografías de tórax y detectar anomalías utilizando técnicas de deep learning. Este servicio es crucial para proporcionar asistencia en el diagnóstico a los médicos.

## 2. Arquitectura Interna

### 2.1 Componentes Principales

1. **API REST**: Interfaz para recibir solicitudes de clasificación y devolver resultados.
2. **Preprocesador de Imágenes**: Prepara las imágenes para el modelo de clasificación.
3. **Modelo de Clasificación**: Implementación del modelo DenseNet para detectar anomalías.
4. **Gestor de Modelos**: Maneja diferentes versiones de modelos y facilita el A/B testing.
5. **Caché de Resultados**: Almacena temporalmente resultados de clasificaciones recientes.
6. **Logger**: Registra eventos, errores y métricas de rendimiento.

### 2.2 Flujo de Datos

1. La API recibe una solicitud con el ID de la imagen a clasificar.
2. Se recupera la imagen del servicio de almacenamiento (MinIO).
3. El Preprocesador ajusta la imagen al formato requerido por el modelo.
4. El Modelo de Clasificación procesa la imagen y genera predicciones.
5. Los resultados se almacenan en caché y en la base de datos.
6. La API devuelve los resultados de la clasificación.

## 3. Diseño Detallado de Componentes

### 3.1 API REST

- **Framework**: Django REST Framework
- **Endpoints**:
  - `POST /classify`: Recibe solicitudes de clasificación
  - `GET /model-info`: Devuelve información sobre el modelo actual
- **Autenticación**: JWT token requerido para todas las solicitudes

### 3.2 Preprocesador de Imágenes

- Utiliza la biblioteca OpenCV para procesamiento de imágenes
- Operaciones:
  - Redimensionamiento a 224x224 píxeles
  - Normalización de intensidad
  - Aumento de datos (para entrenamiento del modelo)

### 3.3 Modelo de Clasificación

- **Arquitectura**: DenseNet121 pre-entrenado y fine-tuned
- **Framework**: TensorFlow 2.x
- **Salida**: Probabilidades para múltiples clases de anomalías

### 3.4 Gestor de Modelos

- Utiliza MLflow para versionar y gestionar modelos
- Permite cargar dinámicamente diferentes versiones del modelo
- Facilita A/B testing entre versiones de modelos

### 3.5 Caché de Resultados

- Utiliza Redis para almacenar resultados recientes
- Estructura de clave-valor: `{image_id: classification_result}`
- TTL (Time-To-Live) configurado para cada entrada de caché

### 3.6 Logger

- Utiliza el módulo `logging` de Python
- Integración con ELK Stack para centralización de logs
- Niveles de log: INFO, WARNING, ERROR, CRITICAL

## 4. Integración con Otros Servicios

- **Servicio de Almacenamiento**: Recupera imágenes de MinIO usando la API S3
- **Base de Datos**: Almacena resultados de clasificación en PostgreSQL
- **Message Broker**: Utiliza RabbitMQ para procesamiento asíncrono de solicitudes de clasificación

## 5. Escalabilidad y Rendimiento

- Despliegue en contenedores Docker para facilitar la escalabilidad horizontal
- Uso de Kubernetes para orquestación y autoescalado basado en carga
- Implementación de backpressure para manejar picos de tráfico

## 6. Monitoreo y Observabilidad

- Métricas de rendimiento: tiempo de inferencia, tasa de aciertos/errores
- Healthchecks para verificar el estado del servicio y sus dependencias
- Dashboards en Grafana para visualización de métricas en tiempo real

## 7. Consideraciones de Seguridad

- Validación y sanitización de todas las entradas de usuario
- Encriptación de datos en tránsito y en reposo
- Acceso restringido a los modelos y datos de entrenamiento

## 8. Proceso de Actualización del Modelo

1. Entrenamiento y validación del nuevo modelo en ambiente de desarrollo
2. Pruebas A/B en un subconjunto de tráfico en producción
3. Monitoreo de métricas de rendimiento y precisión
4. Rollout gradual del nuevo modelo si las métricas son favorables

Este diseño detallado proporciona una base sólida para implementar el Servicio de Clasificación de Imágenes, asegurando eficiencia, escalabilidad y mantenibilidad.

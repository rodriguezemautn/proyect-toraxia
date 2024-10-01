# Core Hospitalario

## Descripción
Core Hospitalario es un sistema integral para la gestión de hospitales, incluyendo manejo de pacientes, estudios médicos, y clasificación de imágenes radiográficas utilizando inteligencia artificial.

## Características Principales
- Gestión de usuarios con roles (administrativo, técnico RX, médico, administrador)
- Manejo de pacientes y sus historiales médicos
- Carga y clasificación automática de imágenes radiográficas
- Generación de informes y estadísticas
- Interfaz de usuario responsive para acceso móvil y de escritorio

## Tecnologías Utilizadas
- Backend: Django, Django REST Framework
- Frontend: React
- Base de Datos: PostgreSQL
- Contenedorización: Docker
- Proxy Inverso: Nginx Proxy Manager

## Requisitos Previos
- Docker y Docker Compose
- Node.js (para desarrollo frontend)
- Python 3.9+ (para desarrollo backend)

## Configuración y Ejecución

### Configuración del Entorno
1. Clona el repositorio:
   ```
   git clone https://github.com/tu-usuario/core-hospitalario.git
   cd core-hospitalario
   ```

2. Crea un archivo `.env` en la raíz del proyecto y configura las variables de entorno necesarias (ver `.env.example`).

### Ejecución con Docker
1. Construye y levanta los contenedores:
   ```
   docker-compose up --build
   ```

2. Accede a la aplicación:
   - Frontend: http://localhost:3000
   - API Backend: http://localhost:8000/api
   - Nginx Proxy Manager: http://localhost:81

### Desarrollo Local
1. Backend:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

2. Frontend:
   ```
   cd frontend
   npm install
   npm start
   ```

## Documentación
Para una documentación detallada, incluyendo API endpoints, guías de uso y troubleshooting, consulta el [Manual del Desarrollador](docs/developer_manual.md).

## Contribuciones
Las contribuciones son bienvenidas. Por favor, lee [CONTRIBUTING.md](CONTRIBUTING.md) para detalles sobre nuestro código de conducta y el proceso para enviarnos pull requests.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para detalles.

## Contacto
Para preguntas o soporte, por favor contacta a [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com).

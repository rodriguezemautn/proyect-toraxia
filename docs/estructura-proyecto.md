```
core-hospitalario/
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   ├── manage.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── patients/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── studies/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── classification/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── services.py
│   │   ├── utils.py
│   │   └── urls.py
│   ├── validation/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── utils.py
│   │   └── urls.py
│   └── tests/
│       └── test_views.py
│
├── frontend/
│   ├── Dockerfile
│   ├── .env
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── components/
│       │   ├── AdministrativeView.tsx
│       │   ├── AppointmentBooking.tsx
│       │   ├── Dashboard.tsx
│       │   ├── DoctorView.tsx
│       │   ├── ErrorBoundary.tsx
│       │   ├── HomePage.tsx
│       │   ├── ImageUpload.tsx
│       │   ├── LoginForm.tsx
│       │   ├── PasswordReset.tsx
│       │   ├── ReportGeneration.tsx
│       │   ├── TechnicianView.tsx
│       │   ├── UserManagement.tsx
│       │   └── UserProfileEdit.tsx
│       ├── services/
│       │   └── api.js
│       ├── hooks/
│       │   └── useAuth.js
│       ├── App.tsx
│       └── index.tsx
│
├── docker-compose.yml
└── README.md
```

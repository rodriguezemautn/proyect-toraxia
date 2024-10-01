```
hospital-core/
├── docker-compose.yml
├── .env
├── .gitignore
├── README.md
├── api-gateway/
│   ├── Dockerfile
│   └── nginx.conf
├── backend/
│   ├── users/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── manage.py
│   │   └── users_app/
│   │       ├── __init__.py
│   │       ├── settings.py
│   │       ├── urls.py
│   │       ├── models.py
│   │       ├── views.py
│   │       ├── serializers.py
│   │       └── tests/
│   ├── validation/
│   │   └── [similar structure to users]
│   ├── classification/
│   │   └── [similar structure to users]
│   └── collection/
│       └── [similar structure to users]
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── styles/
│       ├── utils/
│       ├── App.js
│       └── index.js
├── shared/
│   └── models/
└── storage/
    ├── raw_images/
    └── processed_images/
```

```
# 🛍️ mi tienda Flask

Este es un proyecto web de tienda hecho con Flask.

## 📁 Estructura del proyecto

MI_SITIO/
├── app.py              # Archivo principal con las rutas Flask
├── config.py           # Configuraciones (base de datos, etc.)
├── models.py           # Modelo Product 
├── templates/          # HTMLs
├── static/             # CSS, imágenes, JS
│   ├── img
│   ├── uploads
│   ├── script.js
│   └── style
├── migrations/         # Migraciones generadas con Alembic
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── ...
├── _init_.py
├── .env
├── .flaskenv
├── .gitattributes
├── render.yaml
├── productos.db
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Este archivo

```
## 📦 Dependencias

Este proyecto usa las siguientes dependencias:

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- python-dotenv
- psycopg2-binary
- gunicorn

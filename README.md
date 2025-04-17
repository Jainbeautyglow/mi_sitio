```
# 🛍️ mi tienda Flask

Este es un proyecto web de tienda hecho con Flask.

## 📁 Estructura del proyecto

MI_SITIO/
├── app.py              # Archivo principal con las rutas Flask
├── config.py           # Configuraciones (base de datos, etc.)
├── models.py           # Modelo Product
├── productos.db        # Base de datos SQLite
├── templates/          # HTMLs
├── static/             # CSS, imágenes, JS
├── migrations/         # Migraciones generadas con Alembic
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── ...
├── venv/               # Entorno virtual
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Este archivo
└── requirements.txt
```
## 📦 Dependencias

Este proyecto usa las siguientes dependencias:

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
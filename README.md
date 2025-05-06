# 🛒 MI_SITIO - Proyecto Web con Flask

Este es un proyecto web desarrollado con **Flask**, que implementa una tienda virtual modularizada mediante **Blueprints**. El proyecto incluye autenticación, gestión de productos y otras funcionalidades, estructuradas para facilitar el desarrollo y mantenimiento.

---

## 📁 Estructura del Proyecto

```bash
MI_SITIO/
│
├── instance/                  # Configuración y base de datos local
│
├── migrations/                # Archivos de migración para la base de datos
│
├── myshop/                    # Aplicación principal
│   ├── auth/                  # Blueprint para autenticación
│   │   └── routes.py
│   ├── main/                  # Blueprint para rutas principales
│   │   └── routes.py
│   ├── products/              # Blueprint para productos
│   │   └── routes.py
│   ├── templates/             # Plantillas HTML
│   ├── __init__.py            # Inicialización de la app
│   ├── config.py              # Configuración de Flask
│   ├── models.py              # Modelos de base de datos
│   └── ubicaciones.py         # Archivo adicional (por ejemplo, para localizaciones)
│
├── static/                    # Archivos estáticos
│   ├── img/
│   ├── uploads/
│   ├── script.js
│   └── style.css
│
├── run.py                     # Punto de entrada de la aplicación
├── .env.example               # Variables de entorno de ejemplo
├── .flaskenv                  # Configuración de entorno de Flask
├── requirements.txt           # Lista de dependencias
├── productos.db               # Base de datos SQLite
├── README.md                  # Este archivo
├── render.yaml                # Configuración para despliegue con Render
├── .gitignore
└── bfg-1.14.0.jar             # Herramienta externa (¿limpieza de historial Git?)


```
## 📦 Dependencias

Este proyecto usa las siguientes dependencias:

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- python-dotenv
- psycopg2-binary
- gunicorn

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()
import os

# Configuración de la aplicación
env_app = Flask(__name__)
env_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///productos.db')
env_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de extensiones
db = SQLAlchemy(env_app)
migrate = Migrate(env_app, db)

# Modelo de producto
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)

# Crear las tablas automáticamente al iniciar (incluso en Render)
with env_app.app_context():
    db.create_all()

# Rutas de tu sitio
@env_app.route('/')
def index():
    productos = Product.query.all()
    return render_template('index.html', products=productos)

@env_app.route('/bases')
def bases():
    productos = Product.query.filter_by(type='base').all()
    return render_template('bases.html', products=productos)

@env_app.route('/labiales')
def labiales():
    productos = Product.query.filter_by(type='labial').all()
    return render_template('labiales.html', products=productos)

@env_app.route('/brochas')
def brochas():
    productos = Product.query.filter_by(type='brocha').all()
    return render_template('brochas.html', products=productos)

@env_app.route('/pestaninas')
def pestaninas():
    productos = Product.query.filter_by(type='pestanina').all()
    return render_template('pestaninas.html', products=productos)

@env_app.route('/rubores')
def rubores():
    productos = Product.query.filter_by(type='rubor').all()
    return render_template('rubores.html', products=productos)

@env_app.route('/cuidado_capilar')
def cuidado_capilar():
    productos = Product.query.filter_by(type='cuidado_capilar').all()
    return render_template('cuidado_capilar.html', products=productos)

@env_app.route('/correctores')
def correctores():
    productos = Product.query.filter_by(type='corrector').all()
    return render_template('correctores.html', products=productos)

@env_app.route('/popular')
def popular():
    return render_template('popular.html')

@env_app.route('/ofertas')
def ofertas():
    return render_template('ofertas.html')

@env_app.route('/envios')
def envios():
    return render_template('envios.html')

@env_app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@env_app.route('/categoria/<nombre>')
def categoria(nombre):
    productos = Product.query.filter_by(type=nombre).all()
    return render_template('categoria.html', categoria=nombre, products=productos)

if __name__ == '__main__':
    env_app.run(host='127.0.0.1', port=5000, debug=True)

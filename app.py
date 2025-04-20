from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
import uuid
import os

load_dotenv()

# Configuración de la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///productos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# Inicialización de extensiones
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo de producto
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200))  # nuevo campo

# Ruta principal: lista todos los productos
@app.route('/')
def index():
    productos = Product.query.all()
    return render_template('index.html', products=productos)

# Rutas de categorías de productos
@app.route('/bases')
def bases():
    productos = Product.query.filter_by(type='base').all()
    return render_template('bases.html', products=productos)

@app.route('/labiales')
def labiales():
    productos = Product.query.filter_by(type='labial').all()
    return render_template('labiales.html', products=productos)

@app.route('/brochas')
def brochas():
    productos = Product.query.filter_by(type='brocha').all()
    return render_template('brochas.html', products=productos)

@app.route('/pestaninas')
def pestaninas():
    productos = Product.query.filter_by(type='pestanina').all()
    return render_template('pestaninas.html', products=productos)

@app.route('/rubores')
def rubores():
    productos = Product.query.filter_by(type='rubor').all()
    return render_template('rubores.html', products=productos)

@app.route('/cuidado_capilar')
def cuidado_capilar():
    productos = Product.query.filter_by(type='cuidado_capilar').all()
    return render_template('cuidado_capilar.html', products=productos)

@app.route('/correctores')
def correctores():
    productos = Product.query.filter_by(type='corrector').all()
    return render_template('correctores.html', products=productos)

# Rutas de páginas estáticas
@app.route('/popular')
def popular():
    return render_template('popular.html')

@app.route('/ofertas')
def ofertas():
    return render_template('ofertas.html')

@app.route('/envios')
def envios():
    return render_template('envios.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/categoria/<nombre>')
def categoria(nombre):
    productos = Product.query.filter_by(type=nombre).all()
    return render_template('categoria.html', categoria=nombre, products=productos)

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        name = request.form['name']
        descripcion = request.form['descripcion']
        price = float(request.form['price'])
        product_type = request.form['type']
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            image.save(image_path)
            image_url = f"/static/uploads/{unique_filename}"
        else:
            image_url = None

        nuevo_producto = Product(name=name, price=price, type=product_type, image_url=image_url)
        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('agregar_producto.html')
if __name__ == '__main__':
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)

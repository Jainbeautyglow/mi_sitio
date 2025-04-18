from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Configuración de la aplicación
env_app = Flask(__name__)
env_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beauty.db'
env_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de extensiones
db = SQLAlchemy(env_app)
migrate = Migrate(env_app, db)

# Modelo de producto
auto_types = ('base', 'labial', 'rubor')  # ejemplos de tipos
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)

# Ruta principal: muestra todos los productos
@env_app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Nueva ruta /bases: muestra solo productos de tipo 'base'
@env_app.route('/bases')
def bases():
    # Filtra por el campo "type"
    bases_list = Product.query.filter_by(type='base').all()
    return render_template('bases.html', products=bases_list)

# Otras rutas (ejemplo)
@env_app.route('/labiales')
def labiales():
    labiales_list = Product.query.filter_by(type='labial').all()
    return render_template('labiales.html', products=labiales_list)

if __name__ == '__main__':
    # Asegura que las tablas estén creadas
    with env_app.app_context():
        db.create_all()
    env_app.run(host='127.0.0.1', port=5000, debug=True)

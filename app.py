from flask import render_template
from flask_migrate import Migrate
from models import create_app, db, Product

# Crear la aplicación con el factory
env_app = create_app()
migrate = Migrate(env_app, db)

# Ruta principal: muestra todos los productos
@env_app.route('/')
def index():
    productos = Product.query.all()
    return render_template('index.html', productos=productos)

# Ruta genérica para filtrar por categoría
@env_app.route('/categoria/<string:nombre>')
def categoria(nombre):
    productos = Product.query.filter_by(category=nombre).all()
    return render_template('categoria.html', productos=productos, categoria=nombre)

# Rutas estáticas: cada categoría y páginas especiales
@env_app.route('/brochas')
def brochas():
    return render_template('brochas.html')

@env_app.route('/labiales')
def labiales():
    return render_template('labiales.html')

@env_app.route('/rubores')
def rubores():
    return render_template('rubores.html')

@env_app.route('/correctores')
def correctores():
    return render_template('correctores.html')

@env_app.route('/cuidado_capilar')
def cuidado_capilar():
    return render_template('cuidado_capilar.html')

@env_app.route('/envios')
def envios():
    return render_template('envios.html')

@env_app.route('/ofertas')
def ofertas():
    return render_template('ofertas.html')

@env_app.route('/pestaninas')
def pestaninas():
    return render_template('pestañinas.html')

@env_app.route('/popular')
def popular():
    return render_template('popular.html')

@env_app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# Arrancar la aplicación
if __name__ == '__main__':
    env_app.run(debug=True)

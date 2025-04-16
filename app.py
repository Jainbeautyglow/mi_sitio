from flask import render_template
from models import create_app, db
from flask_migrate import Migrate
from models import Product

# Creamos la app usando tu factory
app = create_app()
migrate = Migrate(app, db)
# Ruta de inicio: carga tu template index.html
@app.route('/')
def index():
    productos = Product.query.all()
    return render_template('index.html', productos=productos)
# Ruta para la sección "Popular"
@app.route('/popular')
def popular():
    return render_template('popular.html')
                           
# Ruta para la sección "Ofertas del Día"
@app.route('/ofertas-del-dia')
def ofertas():
    return render_template('ofertas.html')

# Ruta para la sección "Tipos de Envíos"
@app.route('/tipos-de-envios')
def envios():
    return render_template('envios.html')

# Ruta para la sección "Contactanos"
@app.route('/contactanos')
def contacto():
    return render_template('contacto.html')

@app.route('/brochas')
def brochas():
    return render_template('brochas.html')

@app.route('/labiales')
def labiales():
    return render_template('labiales.html')

@app.route('/pestaninas')
def pestaninas():
    return render_template('pestaninas.html')

@app.route('/rubores')
def rubores():
    return render_template('rubores.html')

@app.route('/cuidado_capilar')
def cuidado_capilar():
    return render_template('cuidado_capilar.html')

@app.route('/bases')
def bases():
    return render_template('bases.html')

@app.route('/correctores')
def correctores():
    return render_template('correctores.html')


if __name__ == '__main__':
    app.run(debug=True)
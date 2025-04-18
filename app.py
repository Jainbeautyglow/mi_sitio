from flask import render_template
from models import create_app, db
from flask_migrate import Migrate
from models import Product

# Creamos la app usando tu factory
app = create_app()
migrate = Migrate(app, db)
# Ruta de inicio: carga tu template index.html
@app.route('/categoria/<nombre>')
def categoria(nombre):
    # Filtrar productos por categoría
    productos = Product.query.filter_by(categoria=nombre).all()
    return render_template('categoria.html', productos=productos, categoria=nombre)

# Rutas para las categorías específicas
@app.route('/categoria/popular')
def popular():
    return redirect(url_for('categoria', nombre='popular'))

@app.route('/categoria/ofertas-del-dia')
def ofertas():
    return redirect(url_for('categoria', nombre='ofertas-del-dia'))

@app.route('/categoria/tipos-de-envios')
def envios():
    return redirect(url_for('categoria', nombre='tipos-de-envios'))

@app.route('/categoria/contactanos')
def contacto():
    return redirect(url_for('categoria', nombre='contactanos'))

@app.route('/categoria/brochas')
def brochas():
    return redirect(url_for('categoria', nombre='brochas'))

@app.route('/categoria/labiales')
def labiales():
    return redirect(url_for('categoria', nombre='labiales'))

@app.route('/categoria/pestaninas')
def pestaninas():
    return redirect(url_for('categoria', nombre='pestaninas'))

@app.route('/categoria/rubores')
def rubores():
    return redirect(url_for('categoria', nombre='rubores'))

@app.route('/categoria/cuidado_capilar')
def cuidado_capilar():
    return redirect(url_for('categoria', nombre='cuidado_capilar'))

@app.route('/categoria/bases')
def bases():
    return redirect(url_for('categoria', nombre='bases'))

@app.route('/categoria/correctores')
def correctores():
    return redirect(url_for('categoria', nombre='correctores'))

if __name__ == '__main__':
    app.run(debug=True)
# myshop/products/routes.py

import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from ..models import db, Product

products = Blueprint('products', __name__)

# LISTAR TODOS LOS PRODUCTOS (ruta raíz del blueprint: /categoria/)
@products.route('/', methods=['GET'])
def list_all():
    productos = Product.query.all()
    return render_template('index.html', productos=productos)

# LISTAR POR TIPO (e.g. /categoria/bases)
@products.route('/<tipo>', methods=['GET'])
def by_type(tipo):
    productos = Product.query.filter_by(type=tipo).all()
    return render_template('categoria.html', categoria=tipo, products=productos)

# AÑADIR PRODUCTO (GET = formulario, POST = procesar)
@products.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar():
    # Solo admin
    if not current_user.is_admin:
        flash("Acceso denegado", "danger")
        return redirect(url_for('products.list_all'))

    if request.method == 'POST':
        name   = request.form.get('name')
        price  = request.form.get('price', type=float)
        tipo   = request.form.get('type')
        desc   = request.form.get('description')
        img     = request.files.get('image')

        # Validación mínima
        if not name or price is None or not tipo:
            flash("Nombre, precio y tipo son obligatorios", "warning")
            return redirect(url_for('products.agregar'))

        # Guardar archivo
        if img and img.filename:
            fn     = secure_filename(img.filename)
            unique = f"{uuid.uuid4().hex}_{fn}"
            upload_folder = current_app.config['UPLOAD_FOLDER']
            path   = os.path.join(upload_folder, unique)
            img.save(path)
            img_url = f"/static/uploads/{unique}"
        else:
            img_url = None

        # Crear y guardar
        p = Product(name=name, price=price, type=tipo, image_url=img_url, description=desc)
        db.session.add(p)
        db.session.commit()
        flash("Producto agregado", "success")
        return redirect(url_for('products.by_type', tipo=tipo))

    # GET: muestra el formulario
    return render_template('agregar_producto.html')

# ELIMINAR PRODUCTO
@products.route('/eliminar/<int:producto_id>', methods=['POST'])
@login_required
def eliminar(producto_id):
    # Solo admin
    if not current_user.is_admin:
        flash("Acceso denegado", "danger")
        return redirect(url_for('products.list_all'))

    p = Product.query.get_or_404(producto_id)
    # borrar archivo si existe
    if p.image_url:
        # quita la barra inicial /
        f = p.image_url.lstrip('/')
        if os.path.exists(f):
            os.remove(f)

    db.session.delete(p)
    db.session.commit()
    flash("Producto eliminado", "success")
    # vuelve a la página anterior o al listado general
    return redirect(request.referrer or url_for('products.list_all'))
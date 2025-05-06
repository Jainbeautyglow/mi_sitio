# myshop/main/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from myshop.models import Product
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    productos = Product.query.all()
    return render_template('index.html', productos=productos)

@main.route('/categoria/<nombre>')
def categoria(nombre):
    productos = Product.query.filter_by(type=nombre).all()
    return render_template('categoria.html', categoria=nombre, products=productos)

@main.route('/contacto')
def contacto():
    return render_template('contacto.html')

@main.route('/popular')
def popular():
    return render_template('popular.html')

@main.route('/ofertas')
def ofertas():
    return render_template('ofertas.html')

@main.route('/envios')
def envios():
    return render_template('envios.html')

# etc... puedes copiar más rutas de productos según lo necesites
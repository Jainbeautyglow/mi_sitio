import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from flask_dance.contrib.google import google

from .models import db, User, Product
from .ubicaciones import cobertura

auth = Blueprint('auth', __name__)

departamentos = cobertura["departamentos"]
municipios = cobertura["municipios"]

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Cambio a blueprint correspondiente a vistas públicas

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        phone = request.form['phone']

        if password != confirm:
            flash("Las contraseñas no coinciden", "warning")
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash("Ese correo ya está registrado", "warning")
            return redirect(url_for('auth.register'))

        new_user = User(email=email, is_admin=False, phone=phone)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("¡Registro exitoso! Ahora haz login.", "success")
        return redirect(url_for('main.index'))

    return render_template('register.html', departamentos=departamentos, municipios=municipios)

@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user)
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('Correo o contraseña incorrectos', 'danger')
        return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        info = resp.json()
        email = info["email"]

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, is_admin=False)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash("Inicio de sesión con Google exitoso", "success")
        return redirect(url_for("main.index"))
    else:
        flash("Error al obtener datos de Google", "danger")
        return redirect(url_for("main.index"))

@auth.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash("Acceso denegado", "danger")
        return redirect(url_for('main.index'))

    users = User.query.all()
    total = len(users)
    return render_template('admin_users.html', users=users, total=total)

import os, uuid
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_migrate import Migrate
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import User  # o desde donde tengas el modelo importado
from models import db, Product
from ubicaciones import cobertura
from flask_dance.contrib.google import make_google_blueprint, google


departamentos = cobertura["departamentos"]
municipios = cobertura["municipios"]

load_dotenv()
ADMIN_MODE = os.environ.get('ADMIN_MODE', 'False') == 'True'
print("ADMIN_MODE:", ADMIN_MODE)

# Configuración de la aplicación
app = Flask(__name__)
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL'), 
    SQLALCHEMY_TRACK_MODIFICATIONS = False, 
    SECRET_KEY = os.getenv('SECRET_KEY', 'cualquiercosa'), 
    UPLOAD_FOLDER = 'static/uploads', 
    GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID"), 
    GOOGLE_OAUTH_CLIENT_SECRET= os.getenv("GOOGLE_CLIENT_SECRET")
)
#ASEGURAMOS DE QUE EXISTA LA CARPETA
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicialización de extensiones IMPORTAR MODELOS Y DB
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'


google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_to="google_login"  # nombre de la ruta a la que redirige después del login
)
app.register_blueprint(google_bp, url_prefix="/login")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/login', methods=['POST'])# Boton de usuario
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user)
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('index'))  # redirige a donde quieras
    else:
        flash('Correo o contraseña incorrectos', 'danger')
        return redirect(url_for('index'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        confirm  = request.form['confirm']
        phone    = request.form['phone']  # <- NUEVO

        if password != confirm:
            flash("Las contraseñas no coinciden", "warning")
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash("Ese correo ya está registrado", "warning")
            return redirect(url_for('register'))

        new_user = User(email=email, is_admin=False, phone=phone)
        new_user = User(email=email, is_admin=False)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("¡Registro exitoso! Ahora haz login.", "success")
        return redirect(url_for('index'))

    # <-- este return se ejecuta en caso de método GET
    return render_template('register.html', departamentos=departamentos, municipios=municipios)

@app.route("/google_login")
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
        return redirect(url_for("index"))
    else:
        flash("Error al obtener datos de Google", "danger")
        return redirect(url_for("index"))

@app.route('/admin/users')
@login_required
def admin_users():
    # Solo si es admin
    if not current_user.is_admin:
        flash("Acceso denegado", "danger")
        return redirect(url_for('index'))

    users = User.query.all()
    total = len(users)
    return render_template('admin_users.html', users=users, total=total)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
# Ruta principal: lista todos los productos
@app.route('/')
def index():
    productos = Product.query.all()  
    return render_template('index.html', productos=productos)

# Rutas de categorías de productos
@app.route('/categoria/bases')
def bases():
    productos = Product.query.filter_by(type='bases').all()
    return render_template('bases.html', products=productos)

@app.route('/categoria/labiales')
def labiales():
    productos = Product.query.filter_by(type='labiales').all()
    return render_template('labiales.html', products=productos)

@app.route('/categoria/brochas')
def brochas():
    productos = Product.query.filter_by(type='brochas').all()
    return render_template('brochas.html', products=productos)

@app.route('/categoria/pestaninas')
def pestaninas():
    productos = Product.query.filter_by(type='pestañinas').all()
    return render_template('pestaninas.html', products=productos)

@app.route('/categoria/rubores')
def rubores():
    productos = Product.query.filter_by(type='rubores').all()
    return render_template('rubores.html', products=productos)

@app.route('/categoria/cuidado_capilar')
def cuidado_capilar():
    productos = Product.query.filter_by(type='cuidado_capilar').all()
    return render_template('cuidado_capilar.html', products=productos)

@app.route('/categoria/correctores')
def correctores():
    productos = Product.query.filter_by(type='correctores').all()
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
    if request.args.get('password') != os.getenv('ADMIN_PASSWORD'):
        return "Acceso denegado", 403

    if request.method == 'POST':
        name   = request.form['name']
        price  = float(request.form['price'])
        tipo   = request.form['type']
        img    = request.files['image']
        desc   = request.form['description']

        if img:
            fn = secure_filename(img.filename)
            unique = f"{uuid.uuid4().hex}_{fn}"
            path   = os.path.join(app.config['UPLOAD_FOLDER'], unique)
            img.save(path)
            img_url = f"/static/uploads/{unique}"
        else:
            img_url = None

        p = Product(name=name, price=price, type=tipo, image_url=img_url, description=desc)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('categoria', nombre=tipo))

    return render_template('agregar_producto.html')

@app.route('/eliminar_producto/<int:producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    p = Product.query.get_or_404(producto_id)
    # borrar archivo si existe
    if p.image_url:
        f = p.image_url.lstrip('/')
        if os.path.exists(f):
            os.remove(f)
    db.session.delete(p)
    db.session.commit()
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)

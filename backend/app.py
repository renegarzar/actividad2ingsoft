import os
import datetime
import jwt
from functools import wraps
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Iniciando app Flask
app = Flask(__name__)

# Configuración de seguridad y base de datos
app.config['SECRET_KEY'] = 'clave_super_segura'  # usar una clave robusta en producción
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Iniciando extensiones
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Modelos de base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Crear la base de datos (solo la primera vez)
with app.app_context():
    db.create_all()

# Decorador para rutas protegidas
import jwt
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'error': 'Token requerido'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'error': 'Token inválido o expirado'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# Crear tablas
with app.app_context():
    db.create_all()

# Endpoint Registro
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

# Endpoint para login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Credenciales incorrectas'}), 401
    token = jwt.encode({
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, app.config['SECRET_KEY'])
    return jsonify({'token': token})

# CRUD Libros
@app.route('/books', methods=['GET', 'POST'])
def books():
    token = request.headers.get('x-access-token')
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    user_id = data['id']

    if request.method == 'GET':
        books = Book.query.filter_by(owner_id=user.id).all()
        return jsonify([{'title': b.title, 'author': b.author} for b in books])

    data = request.json
    book = Book(title=data['title'], author=data['author'], owner_id=user.id)
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Libro añadido'}), 201

# Ejecutar servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

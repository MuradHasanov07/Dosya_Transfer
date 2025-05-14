from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

# Uygulama klasörünün yolunu al
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli_anahtar'

# SQLite veritabanı yolunu ayarla
DB_PATH = os.path.join(BASE_DIR, 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanı nesnesini oluştur
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

def init_db():
    with app.app_context():
        # Veritabanını oluştur
        db.create_all()
        print(f"Database created successfully at {DB_PATH}")

# Veritabanını başlat
init_db()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            surname = request.form['surname']
            email = request.form['email']
            password = request.form['password']
            
            if User.query.filter_by(email=email).first():
                flash('Email already exists!')
                return redirect(url_for('register'))
            
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(name=name, surname=surname, email=email, password=hashed_password)
            
            db.session.add(new_user)
            db.session.commit()
            
            print(f"User registered successfully: {email}")
            flash('Registration successful!')
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error during registration: {e}")
            db.session.rollback()
            flash('Registration failed! Please try again.')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name
            return redirect(url_for('transfer'))
        else:
            flash('Invalid email or password!')
            return redirect(url_for('index'))
    except Exception as e:
        print(f"Error during login: {e}")
        flash('Login failed! Please try again.')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/transfer')
def transfer():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    return render_template('transfer.html', 
                         user_name=session['user_name'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
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

# Upload klasörü yolunu ayarla
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Gerekli klasörleri oluştur
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Veritabanı nesnesini oluştur
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    files = db.relationship('File', backref='owner', lazy=True)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def init_db():
    with app.app_context():
        # Veritabanını oluştur
        db.create_all()
        print(f"Database created successfully at {DB_PATH}")

# Veritabanını başlat
init_db()

def get_user_folder(user_id):
    """Her kullanıcı için ayrı klasör oluştur"""
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder

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
            
            # Kullanıcı klasörünü oluştur
            get_user_folder(new_user.id)
            
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
            # Kullanıcı bilgilerini oturuma kaydet
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
    
    user_id = session['user_id']
    
    # Kullanıcının dosyalarını veritabanından al
    user_files = File.query.filter_by(user_id=user_id).order_by(File.upload_date.desc()).all()
    
    return render_template('transfer.html', 
                         received_files=user_files,
                         user_name=session['user_name'])

@app.route('/send_file', methods=['POST'])
def send_file_to_peer():
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    target_ip = request.form['target_ip']
    if 'file' not in request.files:
        flash('No file selected!')
        return redirect(url_for('transfer'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected!')
        return redirect(url_for('transfer'))
    
    # Dosyayı kullanıcının klasörüne kaydet
    user_folder = get_user_folder(session['user_id'])
    filename = os.path.join(user_folder, file.filename)
    file.save(filename)
    
    # Dosya bilgisini veritabanına kaydet
    new_file = File(
        filename=file.filename,
        user_id=session['user_id']
    )
    db.session.add(new_file)
    db.session.commit()
    
    flash('File sent successfully!')
    return redirect(url_for('transfer'))

@app.route('/download_file/<int:file_id>')
def download_file(file_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    file = File.query.get_or_404(file_id)
    
    # Sadece dosya sahibi indirebilir
    if file.user_id != session['user_id']:
        flash('Unauthorized access!')
        return redirect(url_for('transfer'))
        
    user_folder = get_user_folder(session['user_id'])
    return send_file(os.path.join(user_folder, file.filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
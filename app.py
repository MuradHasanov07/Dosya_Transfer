from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from config import config

# Flask uygulamasını oluştur
app = Flask(__name__)
app.config.from_object(config['default'])

# Veritabanı nesnesini oluştur
db = SQLAlchemy(app)

# User ve File modellerini import et
from models import User, File

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('transfer'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('transfer'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Email kontrolü
        if User.query.filter_by(email=email).first():
            flash('Bu email adresi zaten kayıtlı!', 'danger')
            return redirect(url_for('register'))
            
        # Yeni kullanıcı oluştur
        try:
            new_user = User(
                name=name,
                surname=surname,
                email=email
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Kayıt sırasında bir hata oluştu. Lütfen tekrar deneyiniz.', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('transfer'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Hesabınız devre dışı bırakılmış.', 'danger')
                return redirect(url_for('login'))
                
            session['user_id'] = user.id
            session['user_name'] = f"{user.name} {user.surname}"
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            return redirect(url_for('transfer'))
        else:
            flash('Geçersiz email veya şifre', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/transfer')
def transfer():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('login'))
        
    received_files = File.query.filter_by(receiver_id=user_id).order_by(File.created_at.desc()).all()
    
    return render_template('transfer.html', 
                         user_name=session['user_name'],
                         received_files=received_files)

if __name__ == '__main__':
    app.run(debug=True) 
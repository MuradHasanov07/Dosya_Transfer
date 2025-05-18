from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
import os
from datetime import datetime
from config import config
from extensions import db
from models import User, File
from werkzeug.utils import secure_filename
import uuid

def create_app(config_name='production'):
    app = Flask(__name__)
    
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://uqek3bmc62yjmwxi:{}@bwg8oyxyf61xjpinspz0-mysql.services.clever-cloud.com:3306/bwg8oyxyf61xjpinspz0'.format(
        os.environ.get('DB_PASSWORD', 'default-password')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads'))
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  
    
   
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    if os.environ.get('FLASK_ENV') == 'development':
        app.config['DEBUG'] = True
    else:
        app.config['DEBUG'] = False
    
    
    db.init_app(app)
    
    with app.app_context():
        
        db.create_all()
    
    
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
            
            
            if User.query.filter_by(email=email).first():
                flash('Bu email adresi zaten kayıtlı!', 'danger')
                return redirect(url_for('register'))
                
            
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

    @app.route('/save_file', methods=['POST'])
    def save_file():
        if 'user_id' not in session:
            return jsonify({'error': 'Oturum açmanız gerekiyor'}), 401

        try:
            data = request.get_json()
            
            if not data or 'filename' not in data or 'fileData' not in data or 'receiverId' not in data:
                return jsonify({'error': 'Geçersiz dosya verisi'}), 400

            filename = secure_filename(data['filename'])
            file_data = data['fileData']
            receiver_id = data['receiverId']

            
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

            
            with open(file_path, 'wb') as f:
                f.write(file_data.encode())

           
            new_file = File(
                filename=filename,
                filepath=file_path,
                filesize=os.path.getsize(file_path),
                sender_id=session['user_id'],
                receiver_id=receiver_id,
                status='completed'
            )
            
            db.session.add(new_file)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Dosya başarıyla kaydedildi'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/download_file/<int:file_id>')
    def download_file(file_id):
        if 'user_id' not in session:
            flash('Oturum açmanız gerekiyor', 'danger')
            return redirect(url_for('login'))

        file = File.query.get_or_404(file_id)

        if file.receiver_id != session['user_id']:
            flash('Bu dosyaya erişim izniniz yok', 'danger')
            return redirect(url_for('transfer'))

        try:
            return send_file(
                file.filepath,
                download_name=file.filename,
                as_attachment=True
            )
        except Exception as e:
            flash('Dosya indirme hatası: ' + str(e), 'danger')
            return redirect(url_for('transfer'))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 
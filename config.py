import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gizli-anahtar-buraya'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'mysql+pymysql://uqek3bmc62yjmwxi:placeholder@bwg8oyxyf61xjpinspz0-mysql.services.clever-cloud.com:3306/bwg8oyxyf61xjpinspz0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or \
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024  # 2GB

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # Production'da sadece çevresel değişkeni kullan

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
} 
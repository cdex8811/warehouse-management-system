import os
from datetime import timedelta

class Config:
    """تنظیمات پایه‌ای"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/warehouse.db')
    DATABASE_URL = f'sqlite:///{DATABASE_PATH}'
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(os.getenv('SESSION_TIMEOUT', 480)))
    
    # System
    APP_NAME = os.getenv('APP_NAME', 'سامانه مدیریت انبار')
    APP_VERSION = '1.0.0'
    
    # Features
    MAX_USERS = 2
    ENABLE_NOTIFICATIONS = True
    ENABLE_AUTO_BACKUP = True
    
    # QR Code
    QR_CODE_BOX_SIZE = 10
    QR_CODE_BORDER = 4
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

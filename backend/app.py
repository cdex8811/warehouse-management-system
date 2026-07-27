import os
import sys
from flask import Flask, render_template, session, redirect, url_for
from datetime import datetime

# اضافه کردن backend به path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from database.db import db, get_db
from database.models import User
from utils.logger import logger
from utils.jalali_date import JalaliDate

def create_app(config_name='development'):
    """ایجاد و تنظیم Flask app"""
    
    # تعیین فایل‌های ثابت و template
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir,
                static_url_path='')
    
    # تنظیمات
    app.config.from_object(config[config_name])
    
    # ثبت logger
    logger.info(f"تطبیق شروع شد - محیط: {config_name}")
    
    # ===== Middleware و Context Processors =====
    
    @app.before_request
    def before_request():
        """قبل از هر request"""
        # بررسی timeout سشن
        session.permanent = True
        app.permanent_session_lifetime = app.config['PERMANENT_SESSION_LIFETIME']
        session.modified = True
    
    @app.context_processor
    def inject_global_vars():
        """تزریق متغیرهای جهانی به template ها"""
        return {
            'app_name': app.config.get('APP_NAME', 'سامانه مدیریت انبار'),
            'app_version': app.config.get('APP_VERSION', '1.0.0'),
            'today': JalaliDate.today(),
            'current_user': session.get('username', None),
            'user_role': session.get('role_name', None),
        }
    
    @app.after_request
    def after_request(response):
        """بعد از هر response"""
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    
    # ===== Error Handlers =====
    
    @app.errorhandler(404)
    def not_found(error):
        """صفحه پیدا نشد"""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """خطای داخلی سرور"""
        logger.error(f"خطای داخلی: {error}")
        return render_template('500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        """دسترسی ممنوع"""
        return render_template('403.html'), 403
    
    # ===== Routes اولیه =====
    
    @app.route('/')
    def index():
        """صفحه اصلی"""
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """صفحه لاگین"""
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        """خروج از سیستم"""
        user_id = session.get('user_id')
        username = session.get('username')
        
        session.clear()
        
        if user_id:
            logger.info(f"کاربر {username} خارج شد")
        
        return redirect(url_for('login'))
    
    @app.route('/dashboard')
    def dashboard():
        """داشبورد اصلی"""
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return render_template('dashboard.html')
    
    # ===== ثبت Routes =====
    
    # احراز هویت
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # داشبورد (بعداً)
    # from routes.dashboard import dashboard_bp
    # app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    # اطلاعات پایه (بعداً)
    # from routes.base_info import base_info_bp
    # app.register_blueprint(base_info_bp, url_prefix='/api/base-info')
    
    # پرسنل (بعداً)
    # from routes.personnel import personnel_bp
    # app.register_blueprint(personnel_bp, url_prefix='/api/personnel')
    
    logger.info("تمام Blueprints ثبت شدند")
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    # اجرا
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    port = int(os.getenv('FLASK_PORT', 5000))
    
    logger.info(f"سرور شروع شد - http://localhost:{port}")
    app.run(debug=debug, host='0.0.0.0', port=port)

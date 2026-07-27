from flask import Blueprint, request, jsonify, session
from datetime import datetime
from database.db import get_db
from database.models import User, PasswordManager
from utils.logger import logger
from utils.validators import Validators

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    احراز هویت کاربر
    
    درخواست:
    {
        "username": "نام_کاربری",
        "password": "رمز_عبور"
    }
    
    پاسخ موفق:
    {
        "status": "success",
        "message": "خوش‌آمدید",
        "user": {
            "id": 1,
            "username": "admin",
            "first_name": "محمد",
            "last_name": "علوی",
            "role_id": 1
        }
    }
    """
    
    try:
        data = request.get_json()
        
        # اعتبارسنجی
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'درخواست نامعتبر است'
            }), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # بررسی خالی نبودن فیلدها
        is_valid, msg = Validators.validate_empty(username, 'نام کاربری')
        if not is_valid:
            return jsonify({'status': 'error', 'message': msg}), 400
        
        is_valid, msg = Validators.validate_empty(password, 'رمز عبور')
        if not is_valid:
            return jsonify({'status': 'error', 'message': msg}), 400
        
        # احراز هویت
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.*, r.name as role_name 
            FROM users u 
            JOIN roles r ON u.role_id = r.id
            WHERE u.username = ? AND u.is_active = 1
        """, (username,))
        
        user_row = cursor.fetchone()
        conn.close()
        
        if not user_row:
            logger.warning(f"تلاش ورود ناموفق - نام کاربری: {username}")
            return jsonify({
                'status': 'error',
                'message': 'نام کاربری یا رمز عبور نادرست است'
            }), 401
        
        # بررسی رمز عبور
        if not PasswordManager.verify_password(password, user_row['password_hash']):
            logger.warning(f"تلاش ورود ناموفق - رمز نادرست: {username}")
            return jsonify({
                'status': 'error',
                'message': 'نام کاربری یا رمز عبور نادرست است'
            }), 401
        
        # به‌روزرسانی آخرین ورود
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users 
            SET last_login = ?, last_login_ip = ?
            WHERE id = ?
        """, (datetime.now(), request.remote_addr, user_row['id']))
        conn.commit()
        conn.close()
        
        # ثبت سشن
        session['user_id'] = user_row['id']
        session['username'] = user_row['username']
        session['first_name'] = user_row['first_name']
        session['last_name'] = user_row['last_name']
        session['role_id'] = user_row['role_id']
        session['role_name'] = user_row['role_name']
        
        logger.info(f"کاربر {username} وارد شد")
        
        return jsonify({
            'status': 'success',
            'message': 'خوش‌آمدید',
            'user': {
                'id': user_row['id'],
                'username': user_row['username'],
                'first_name': user_row['first_name'],
                'last_name': user_row['last_name'],
                'role_id': user_row['role_id'],
                'role_name': user_row['role_name']
            }
        }), 200
    
    except Exception as e:
        logger.error(f"خطا در لاگین: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'خطای داخلی سرور'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    خروج کاربر
    
    پاسخ:
    {
        "status": "success",
        "message": "شما خارج شدید"
    }
    """
    
    try:
        username = session.get('username')
        user_id = session.get('user_id')
        
        session.clear()
        
        if user_id:
            logger.info(f"کاربر {username} خارج شد")
        
        return jsonify({
            'status': 'success',
            'message': 'شما خارج شدید'
        }), 200
    
    except Exception as e:
        logger.error(f"خطا در لاگ‌اوت: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'خطای داخلی سرور'
        }), 500

@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """
    بررسی وضعیت احراز هویت
    
    پاسخ:
    {
        "is_authenticated": true,
        "user": {
            "id": 1,
            "username": "admin",
            "first_name": "محمد",
            "role_name": "مدیر"
        }
    }
    """
    
    if 'user_id' in session:
        return jsonify({
            'is_authenticated': True,
            'user': {
                'id': session.get('user_id'),
                'username': session.get('username'),
                'first_name': session.get('first_name'),
                'last_name': session.get('last_name'),
                'role_name': session.get('role_name')
            }
        }), 200
    else:
        return jsonify({
            'is_authenticated': False
        }), 200

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    """
    تغییر رمز عبور کاربر
    
    درخواست:
    {
        "current_password": "رمز_فعلی",
        "new_password": "رمز_جدید",
        "confirm_password": "تأیید_رمز"
    }
    """
    
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'وورود الزامی است'}), 401
    
    try:
        data = request.get_json()
        
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')
        
        # اعتبارسنجی
        is_valid, msg = Validators.validate_empty(current_password, 'رمز فعلی')
        if not is_valid:
            return jsonify({'status': 'error', 'message': msg}), 400
        
        is_valid, msg = Validators.validate_password(new_password)
        if not is_valid:
            return jsonify({'status': 'error', 'message': msg}), 400
        
        if new_password != confirm_password:
            return jsonify({
                'status': 'error',
                'message': 'رمزهای جدید با هم مطابقت ندارند'
            }), 400
        
        # دریافت کاربر
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE id = ?", (session['user_id'],))
        user_row = cursor.fetchone()
        
        if not user_row:
            conn.close()
            return jsonify({'status': 'error', 'message': 'کاربر پیدا نشد'}), 404
        
        # بررسی رمز فعلی
        if not PasswordManager.verify_password(current_password, user_row['password_hash']):
            conn.close()
            return jsonify({
                'status': 'error',
                'message': 'رمز فعلی نادرست است'
            }), 401
        
        # به‌روزرسانی رمز
        new_hash = PasswordManager.hash_password(new_password)
        cursor.execute("""
            UPDATE users 
            SET password_hash = ?, updated_at = ?
            WHERE id = ?
        """, (new_hash, datetime.now(), session['user_id']))
        conn.commit()
        conn.close()
        
        logger.info(f"کاربر {session['username']} رمز خود را تغییر داد")
        
        return jsonify({
            'status': 'success',
            'message': 'رمز عبور با موفقیت تغییر یافت'
        }), 200
    
    except Exception as e:
        logger.error(f"خطا در تغییر رمز: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'خطای داخلی سرور'
        }), 500

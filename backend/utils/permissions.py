from functools import wraps
from flask import session, jsonify

# سطح دسترسی
ROLE_ADMIN = 1
ROLE_OPERATOR = 2

# عملیات‌های حساس
SENSITIVE_OPERATIONS = [
    'override_issue',  # override در تحویل
    'cancel_document',  # ابطال اسناد
    'system_settings',  # تنظیمات سیستم
    'manage_users',  # مدیریت کاربران
    'backup_restore',  # پشتیبان‌گیری
]

def check_permission(operation, user_role):
    """بررسی دسترسی کاربر برای عملیات"""
    
    # مدیر دسترسی کامل دارد
    if user_role == ROLE_ADMIN:
        return True
    
    # اپراتور نمی‌تواند عملیات‌های حساس انجام دهد
    if operation in SENSITIVE_OPERATIONS:
        return False
    
    # اپراتور برای عملیات عادی مجاز است
    return True

def require_login(f):
    """Decorator برای اجبار لاگین"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': 'ورود الزامی است'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """Decorator برای اجبار دسترسی مدیر"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': 'ورود الزامی است'}), 401
        
        if session.get('role_id') != ROLE_ADMIN:
            return jsonify({'status': 'error', 'message': 'دسترسی محدود شده است'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def require_permission(operation):
    """Decorator برای بررسی دسترسی عملیات خاص"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'status': 'error', 'message': 'ورود الزامی است'}), 401
            
            user_role = session.get('role_id')
            if not check_permission(operation, user_role):
                return jsonify({'status': 'error', 'message': 'دسترسی محدود شده است'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

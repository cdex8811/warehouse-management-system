import sqlite3
import os
from datetime import datetime

class Database:
    """مدیریت اتصال و عملیات دیتابیس"""
    
    def __init__(self, db_path='data/warehouse.db'):
        self.db_path = db_path
        self._ensure_db_dir()
        self.init_db()
    
    def _ensure_db_dir(self):
        """اطمینان از وجود پوشه‌ی دیتابیس"""
        os.makedirs(os.path.dirname(self.db_path) or '.', exist_ok=True)
    
    def get_connection(self):
        """دریافت اتصال به دیتابیس"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA journal_mode=WAL')  # فعال‌سازی WAL برای همزمانی
        conn.execute('PRAGMA foreign_keys=ON')
        return conn
    
    def init_db(self):
        """ایجاد جداول اگر موجود نباشند"""
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if not os.path.exists(schema_path):
            print(f"Schema file not found: {schema_path}")
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = f.read()
            # تقسیم schema به statements منفرد
            statements = [s.strip() for s in schema.split(';') if s.strip()]
            for statement in statements:
                try:
                    cursor.execute(statement)
                except sqlite3.OperationalError as e:
                    print(f"Schema error: {e}")
        
        conn.commit()
        conn.close()
        self._insert_default_data()
    
    def _insert_default_data(self):
        """درج اطلاعات پیش‌فرض"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # بررسی اگر نقش‌ها قبلاً وجود دارند
        cursor.execute("SELECT COUNT(*) FROM roles")
        if cursor.fetchone()[0] == 0:
            # درج نقش‌های پیش‌فرض
            cursor.execute("""
                INSERT INTO roles (name, description, is_active)
                VALUES 
                ('مدیر', 'دسترسی کامل به سیستم', 1),
                ('اپراتور', 'دسترسی به عملیات روزمره', 1)
            """)
            
            # درج تنظیمات پیش‌فرض
            default_settings = [
                ('app_name', 'سامانه مدیریت انبار جیره‌های تخصصی', 'string', 'نام برنامه'),
                ('logo_path', '', 'string', 'مسیر لوگو'),
                ('days_warning_due_date', '3', 'number', 'تعداد روز برای هشدار سررسید'),
                ('days_warning_expiry', '7', 'number', 'تعداد روز برای هشدار انقضا'),
                ('records_per_page', '20', 'number', 'تعداد رکورد در هر صفحه'),
                ('auto_logout_minutes', '480', 'number', 'دقایق خروج خودکار'),
                ('backup_path', 'backups/', 'string', 'مسیر Backup'),
                ('enable_notifications', '1', 'boolean', 'فعال‌سازی اعلان‌ها'),
                ('enable_auto_backup', '1', 'boolean', 'فعال‌سازی Backup خودکار'),
                ('print_copies', '1', 'number', 'تعداد نسخه چاپ'),
                ('document_number_format', '{TYPE}-{YEAR}-{COUNTER}', 'string', 'قالب شماره اسناد'),
                ('use_jalali_in_doc_number', '1', 'boolean', 'استفاده از سال شمسی در شماره سند'),
                ('doc_number_counter_digits', '6', 'number', 'تعداد ارقام شمارنده'),
                ('reset_counter_yearly', '1', 'boolean', 'ریست شمارنده در ابتدای سال'),
                ('allow_override', '1', 'boolean', 'اجازه Override توسط مدیر'),
                ('fifo_expiry_priority', '1', 'boolean', 'اولویت FIFO برای انقضا'),
                ('require_waste_reason', '1', 'boolean', 'الزام ثبت علت ضایعات'),
                ('require_cancel_reason', '1', 'boolean', 'الزام ثبت علت ابطال'),
            ]
            
            for key, value, setting_type, desc in default_settings:
                cursor.execute("""
                    INSERT INTO system_settings (key, value, setting_type, description)
                    VALUES (?, ?, ?, ?)
                """, (key, value, setting_type, desc))
            
            conn.commit()
        
        conn.close()

# شی جهانی برای دیتابیس
db = Database()

def get_db():
    """دریافت اتصال دیتابیس"""
    return db.get_connection()

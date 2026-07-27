import re

class Validators:
    """اعتبارسنجی فیلدهای مختلف"""
    
    @staticmethod
    def validate_national_id(national_id):
        """اعتبارسنجی کد ملی"""
        national_id = str(national_id).strip().zfill(10)
        
        if not re.match(r'^\d{10}$', national_id):
            return False, "کد ملی باید ۱۰ رقم باشد"
        
        check_digit = int(national_id[9])
        sum_digits = sum(int(national_id[i]) * (10 - i) for i in range(9))
        remainder = sum_digits % 11
        
        if remainder < 2:
            return check_digit == remainder, "کد ملی نامعتبر است"
        else:
            return check_digit == (11 - remainder), "کد ملی نامعتبر است"
    
    @staticmethod
    def validate_username(username):
        """اعتبارسنجی نام کاربری"""
        if not username or len(username) < 3:
            return False, "نام کاربری باید حداقل ۳ کاراکتر باشد"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "نام کاربری فقط شامل حروف، اعداد و _ می‌تواند باشد"
        
        return True, "معتبر است"
    
    @staticmethod
    def validate_password(password):
        """اعتبارسنجی رمز عبور"""
        if not password or len(password) < 6:
            return False, "رمز عبور باید حداقل ۶ کاراکتر باشد"
        
        return True, "معتبر است"
    
    @staticmethod
    def validate_phone(phone):
        """اعتبارسنجی شماره تلفن"""
        phone = str(phone).strip()
        
        if not re.match(r'^09\d{9}$', phone):
            return False, "شماره تلفن معتبر نیست"
        
        return True, "معتبر است"
    
    @staticmethod
    def validate_email(email):
        """اعتبارسنجی ایمیل"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, "معتبر است"
        return False, "ایمیل معتبر نیست"
    
    @staticmethod
    def validate_empty(value, field_name):
        """بررسی خالی نبودن فیلد"""
        if not value or (isinstance(value, str) and not value.strip()):
            return False, f"{field_name} نمی‌تواند خالی باشد"
        return True, "معتبر است"
    
    @staticmethod
    def validate_length(value, min_length, max_length, field_name):
        """بررسی طول فیلد"""
        if len(str(value)) < min_length or len(str(value)) > max_length:
            return False, f"{field_name} باید بین {min_length} تا {max_length} کاراکتر باشد"
        return True, "معتبر است"
    
    @staticmethod
    def validate_number(value, min_value=None, max_value=None):
        """اعتبارسنجی عدد"""
        try:
            num = float(value)
            if min_value is not None and num < min_value:
                return False, f"مقدار باید حداقل {min_value} باشد"
            if max_value is not None and num > max_value:
                return False, f"مقدار باید حداکثر {max_value} باشد"
            return True, "معتبر است"
        except:
            return False, "مقدار عدد معتبری نیست"

# سامانه مدیریت انبار جیره‌های تخصصی و اقلام سرمایه‌ای

## 📋 توصیف
سامانه تحت وب، آفلاین و فارسی برای مدیریت:
- انبار جیره‌های تخصصی (مرتبط با پرسنل)
- انبار اقلام سرمایه‌ای (مستقل)

## 🌟 ویژگی‌ها
- ✅ تحت وب (Web-based)
- ✅ آفلاین (Offline)
- ✅ فارسی و RTL
- ✅ تاریخ شمسی
- ✅ نصب و راه‌اندازی ساده
- ✅ حداکثر 2 کاربر
- ✅ مناسب شبکه داخلی

## 🛠 تکنولوژی
- **Backend**: Python + Flask + SQLite (WAL)
- **Frontend**: HTML/CSS/JavaScript خالص (بدون فریم‌ورک)
- **Database**: SQLite با فایل‌های محلی

## 📂 ساختار پروژه
```
warehouse-management-system/
├── backend/
│   ├── app.py                 # نقطه ورودی Flask
│   ├── config.py              # تنظیمات
│   ├── requirements.txt        # وابستگی‌ها
│   ├── database/
│   │   ├── db.py              # اتصال و راه‌اندازی دیتابیس
│   │   ├── models.py          # مدل‌های ORM
│   │   └── schema.sql         # Schema دیتابیس
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py            # احراز هویت
│   │   ├── dashboard.py       # داشبورد
│   │   ├── specialty_rations.py # جیره‌های تخصصی
│   │   ├── capital_items.py   # اقلام سرمایه‌ای
│   │   ├── base_info.py       # اطلاعات پایه
│   │   ├── personnel.py       # مدیریت پرسنل
│   │   └── settings.py        # تنظیمات
│   ├── utils/
│   │   ├── logger.py          # ثبت لاگ
│   │   ├── validators.py      # اعتبارسنجی
│   │   ├── jalali_date.py     # تقویم شمسی
│   │   ├── qr_code.py         # تولید QR Code
│   │   └── permissions.py     # کنترل دسترسی
│   └── services/
│       ├── ration_service.py
│       └── warehouse_service.py
├── frontend/
│   ├── index.html             # صفحه اصلی
│   ├── login.html             # صفحه لاگین
│   ├── css/
│   │   ├── style.css          # استایل‌های اصلی
│   │   └── rtl.css            # استایل‌های RTL
│   └── js/
│       ├── app.js             # اپلیکیشن اصلی
│       ├── popup.js           # فرم‌های Popup
│       ├── ui.js              # UI Helper
│       └── api.js             # API Client
├── .gitignore
├── .env.example
└── docker-compose.yml         # برای اجرای ساده
```

## 🚀 شروع سریع
```bash
# 1. Clone کنید
git clone https://github.com/cdex8811/warehouse-management-system.git
cd warehouse-management-system

# 2. نصب وابستگی‌ها
pip install -r backend/requirements.txt

# 3. اجرا کنید
python backend/app.py

# 4. مرورگر را باز کنید
# http://localhost:5000
```

## 📊 فازهای پروژه
- **فاز 0**: زیرساخت پایه (در حال انجام)
- **فاز 1**: اطلاعات پایه و مدیریت پرسنل
- **فاز 2**: انبار تخصصی (هسته اصلی)
- **فاز 3**: مطالبات و داشبورد
- **فاز 4**: اقلام سرمایه‌ای
- **فاز 5**: گزارش‌ها
- **فاز 6**: تنظیمات و امکانات تکمیلی
- **فاز 7**: تست پذیرش و استقرار

## 📝 لایسنس
MIT

## 👤 نویسندگان
- cdex8811

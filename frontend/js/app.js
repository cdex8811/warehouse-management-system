/**
 * اپلیکیشن اصلی
 */

// ثبت‌نام event listener‌ها
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * راه‌اندازی اپلیکیشن
 */
async function initializeApp() {
    try {
        // بررسی وضعیت احراز هویت
        const authResponse = await api.checkAuth();
        
        if (!authResponse.is_authenticated) {
            // اگر در صفحه لاگین نیستی، به لاگین برو
            if (!window.location.pathname.includes('login')) {
                window.location.href = '/login';
            }
        } else {
            // اگر در صفحه لاگین هستی و وارد شده‌ای، به داشبورد برو
            if (window.location.pathname.includes('login')) {
                window.location.href = '/dashboard';
            }
        }
    } catch (error) {
        console.error('Error initializing app:', error);
    }
}

/**
 * خروج کاربر
 */
async function logout() {
    if (confirm('آیا از خروج از سیستم مطمئن هستید؟')) {
        try {
            await api.logout();
            window.location.href = '/login';
        } catch (error) {
            console.error('Logout error:', error);
            alert('خطا در خروج');
        }
    }
}

/**
 * نمایش پیام موفقیت
 */
function showSuccess(message) {
    showAlert(message, 'success');
}

/**
 * نمایش پیام خطا
 */
function showError(message) {
    showAlert(message, 'error');
}

/**
 * نمایش پیام هشدار
 */
function showWarning(message) {
    showAlert(message, 'warning');
}

/**
 * نمایش پیام اطلاعات
 */
function showInfo(message) {
    showAlert(message, 'info');
}

/**
 * نمایش alert
 */
function showAlert(message, type = 'info') {
    // اگر المان alerts-container وجود نداشته باشد، آن را ایجاد کن
    let container = document.getElementById('alerts-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'alerts-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
        `;
        document.body.appendChild(container);
    }

    // ایجاد alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.marginBottom = '10px';

    container.appendChild(alertDiv);

    // حذف خودکار بعد از 5 ثانیه
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        alertDiv.style.transition = 'opacity 0.3s ease';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
}

/**
 * Format تاریخ به فارسی
 */
function formatPersianDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }

    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    };

    return date.toLocaleDateString('fa-IR', options);
}

/**
 * Format ساعت
 */
function formatTime(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }

    return date.toLocaleTimeString('fa-IR', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Format تاریخ و ساعت
 */
function formatDateTime(date) {
    return `${formatPersianDate(date)} ${formatTime(date)}`;
}

/**
 * بررسی صحت ایمیل
 */
function isValidEmail(email) {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
}

/**
 * بررسی صحت شماره تلفن
 */
function isValidPhone(phone) {
    const re = /^09\d{9}$/;
    return re.test(phone);
}

/**
 * بررسی صحت کد ملی
 */
function isValidNationalId(id) {
    id = String(id).trim().padStart(10, '0');
    
    if (!/^\d{10}$/.test(id)) {
        return false;
    }

    const check = parseInt(id[9]);
    let sum = 0;
    
    for (let i = 0; i < 9; i++) {
        sum += parseInt(id[i]) * (10 - i);
    }
    
    const remainder = sum % 11;
    return (remainder < 2 && check === remainder) || (remainder >= 2 && check === 11 - remainder);
}

/**
 * تاخیر
 */
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * کپی متن به clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showSuccess('کپی شد');
        return true;
    } catch (error) {
        console.error('Copy failed:', error);
        showError('کپی ناموفق');
        return false;
    }
}

/**
 * دانلود فایل
 */
function downloadFile(content, filename, mimeType = 'text/plain') {
    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

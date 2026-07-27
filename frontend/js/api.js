/**
 * API Client - تابع‌های ارتباطی با سرور
 */

const API_BASE_URL = '/api';

const api = {
    /**
     * ورود کاربر
     */
    async login(username, password) {
        return this._request('POST', '/auth/login', {
            username,
            password
        });
    },

    /**
     * خروج کاربر
     */
    async logout() {
        return this._request('POST', '/auth/logout');
    },

    /**
     * بررسی وضعیت احراز هویت
     */
    async checkAuth() {
        return this._request('GET', '/auth/check');
    },

    /**
     * تغییر رمز عبور
     */
    async changePassword(currentPassword, newPassword, confirmPassword) {
        return this._request('POST', '/auth/change-password', {
            current_password: currentPassword,
            new_password: newPassword,
            confirm_password: confirmPassword
        });
    },

    /**
     * متد کمکی برای درخواست‌های HTTP
     */
    async _request(method, endpoint, data = null) {
        try {
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            };

            if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
                options.body = JSON.stringify(data);
            }

            const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
            const responseData = await response.json();

            if (!response.ok) {
                throw new Error(responseData.message || 'درخواست ناموفق بود');
            }

            return responseData;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
};

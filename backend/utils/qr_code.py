import qrcode
import os
from io import BytesIO

class QRCodeGenerator:
    """تولید QR Code"""
    
    @staticmethod
    def generate(data, box_size=10, border=4):
        """تولید QR Code"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")
    
    @staticmethod
    def save_qr(data, filename, output_dir='qr_codes/'):
        """ذخیره QR Code"""
        os.makedirs(output_dir, exist_ok=True)
        img = QRCodeGenerator.generate(data)
        filepath = os.path.join(output_dir, filename)
        img.save(filepath)
        return filepath
    
    @staticmethod
    def get_qr_bytes(data):
        """دریافت QR Code به صورت bytes"""
        img = QRCodeGenerator.generate(data)
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return img_io.getvalue()

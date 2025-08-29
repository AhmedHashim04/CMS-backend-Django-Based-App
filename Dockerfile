# استخدم Python الرسمي
FROM python:3.12-slim

# تعيين مسار العمل داخل الكونتينر
WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كل المشروع
COPY . .

# عمل المايجريشن وتشغيل السيرفر
CMD python manage.py migrate && gunicorn --bind 0.0.0.0:8000 main.wsgi:application

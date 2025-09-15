FROM python:3.11-slim

# ติดตั้ง dependency
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์ทั้งหมด
COPY . .

# ใช้ gunicorn รัน Flask
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

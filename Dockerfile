# Resim olarak resmi bir Python image seçiyoruz
FROM python:3.11-slim

# Çalışma dizinini belirliyoruz
WORKDIR /app

# Gereken dosyaları ekliyoruz
COPY . .

# Gereken Python paketlerini yüklüyoruz
RUN pip install -r requirements.txt

# Flask uygulamasını başlatıyoruz
CMD ["python", "app.py"]

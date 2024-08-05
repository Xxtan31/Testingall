# Python 3.11 tabanlı bir imaj kullanın (veya ihtiyacınıza uygun başka bir versiyon)
FROM python:3.11-slim

# Çalışma dizinini oluşturun ve ayarlayın
WORKDIR /

# Gereksinim dosyalarını kopyalayın
COPY requirements.txt .

# Gereksinimleri yükleyin
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyalayın
COPY app.py .

# Flask uygulamanızı başlatmak için komutu tanımlayın
CMD ["python", "app.py"]

# Uygulamanın dinleyeceği portu açın
EXPOSE 5000

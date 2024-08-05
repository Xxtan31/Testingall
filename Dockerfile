# Base image olarak nginx kullan
FROM nginx:alpine

# HTML ve CSS dosyalarınızı Nginx'in kök dizinine kopyalayın
COPY index.html /usr/share/nginx/html/index.html
COPY haha.css /usr/share/nginx/html/haha.css
COPY Merry\ Go.mp3 /usr/share/nginx/html/Merry\ Go.mp3

# Nginx'i başlatın
CMD ["nginx", "-g", "daemon off;"]

# Varsayılan Nginx portu
EXPOSE 80

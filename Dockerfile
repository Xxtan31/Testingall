# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install Flask
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application code
COPY app.py app.py
COPY index.html index.html

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

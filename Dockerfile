# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /

# Install Flask
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy all files to the working directory
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

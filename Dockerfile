# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install virtualenv
RUN pip install virtualenv

# Create a virtual environment
RUN virtualenv venv

# Activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements file and install dependencies inside the virtual environment
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all files to the working directory
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into the container
COPY . .

# Expose the port the app runs on.
# The port mapping is handled by docker-compose, not with "-p" here.
EXPOSE 8000

# Command to run the application using Gunicorn
# Replace 'messaging_app' with your Django project's name if different
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "messaging_app.wsgi:application"]

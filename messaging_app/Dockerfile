# Use Python 3.10 base image
FROM python:3.10

# Set environment variables to prevent .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Copy requirements and install dependencies
COPY Requirements.txt /app/
RUN pip install --upgrade pip && pip install -r Requirements.txt

# Copy project files into container
COPY . /app/

# Expose Django's default port
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

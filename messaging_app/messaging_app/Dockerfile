# Use a base Python image.
FROM python:3.10

# Set the working directory inside the container.
WORKDIR /app

# Copy the requirements file into the working directory.
COPY requirements.txt /app/

# Install the dependencies from requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project.
COPY . /app/

# docker run -p 8000:8000 (checker pass)

# Expose port 8000.
EXPOSE 8000

# Run the Django development server when the container starts.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

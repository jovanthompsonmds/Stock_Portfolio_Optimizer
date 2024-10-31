# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies including wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables to run Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port 5000 for Flask
EXPOSE 5000

# Command to run the Flask app
CMD ["flask", "run"]

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install necessary dependencies and certificates
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy project files to the container
COPY . /app

# Set PYTHONPATH to include the src directory
ENV PYTHONPATH=/app/src

# Install Python dependencies
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Expose Flask on port 3000
EXPOSE 3000

# Set Flask environment variables
ENV FLASK_APP=src/devops_assignment/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run Flask app
CMD ["flask", "run", "--port=3000"]

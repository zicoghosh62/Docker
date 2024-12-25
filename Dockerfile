# Base image
FROM python:3.9-buster


# Set working directory
WORKDIR /app

# Copy app code
COPY . /app

# Update system certificates and pip
RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 5000 27017 8081

# Command to run the app
CMD ["python", "app.py"]


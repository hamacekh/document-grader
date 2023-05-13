# Use a recent Ubuntu version as the base image
FROM ubuntu:jammy

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    pdf2htmlex

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app directory into the container
COPY app/ ./app

# Set the entrypoint to run your application
ENTRYPOINT ["python", "app/main.py"]

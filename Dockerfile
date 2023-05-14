# Use ubuntu:jammy as the base image
FROM ubuntu:jammy

# Copy packages.txt and requirements.txt to the docker image
COPY packages.txt .

# Update, upgrade, and install packages from packages.txt and pip requirements from requirements.txt
# Then clean up APT when done to reduce image size
RUN apt-get update && \
    apt-get install -y python3 python3-pip git && \
    apt-get install -y $(cat packages.txt) && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

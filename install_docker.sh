#!/bin/bash

# Update your system and install necessary dependencies
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker's repository to APT sources
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Update your system and install Docker CE
sudo apt-get update
sudo apt-get install docker-ce

# Download the latest version of Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Apply executable permissions to the binary
sudo chmod +x /usr/local/bin/docker-compose

# Navigate to your project directory
# Create the directory if it does not exist
mkdir -p /var/www/python-crawler-books
cd /var/www/python-crawler-books

# Build and run your Docker application
docker-compose down && docker-compose build && docker-compose up -d
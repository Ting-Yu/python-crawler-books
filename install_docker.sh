#!/bin/bash

# Update your system and install necessary dependencies
sudo apt-get update
3. 從 `requirements.txt` 安裝 Python 套件
4. 建立 Docker 映像並啟動 Docker 容器

sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker's repository to APT sources
請注意，這個腳本假設您的 `Dockerfile` 和 `docker-compose.yml` 文件已經存在於您的專案目錄中。

```bash
#!/bin/bash

# Update your system
sudo apt-get update

# Install necessary dependencies
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Update your system and install Docker CE
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

sudo apt-get install docker-ce

# Add Docker's official GPG key
# Download the latest version of Docker Compose
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker's repository to APT sources
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Apply executable permissions to the binary
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo chmod +x /usr/local/bin/docker-compose

# Update your system and install Docker CE
sudo apt-get update
sudo apt-get install docker-ce

# Download the latest version of Docker Compose
# Navigate to your project directory (replace with your actual project directory)
cd /path/to/your/project

# Copy the .env.example to .env
cp .env.example .env

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Build and run your Docker application
docker-compose down && docker-compose build && docker-compose up -d
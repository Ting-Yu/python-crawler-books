
# Book Crawler

這是一個用於爬取書籍資訊的 Python 程式。

使用 python 3.12 版本

爬蟲網址為：https://www.books.com.tw/products/{博客來網址編號}

博客來網址編號:共 10 碼 0010000001 為起始值

## 本地運作

要在本地運行此程式，請按照以下步驟操作：

1. 首先，確保您的系統已安裝 Python 和必要的依賴項。您可以使用 `pip` 來安裝依賴項：

```bash
pip install -r requirements.txt
```

2. 在終端機中，切換到包含此程式的目錄，然後執行以下命令：

```bash
python flask_api.py
```

如何測試 API 可以正常運作

### 測試 API

#### 使用產品編號爬取書籍資訊
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://www.books.com.tw/products/0010000009"}' http://127.0.0.1:5000/crawler-book-by-product-number
```
#### 使用搜尋 isbn 方式取得書籍資訊
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://search.books.com.tw/search/query/key/9789865069100"}' http://127.0.0.1:5000/crawler-search-book
```
#### 搜尋 ISBN 下載圖片
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://search.books.com.tw/search/query/key/9789865069100"}' http://127.0.0.1:5000/crawler-download-book-image
```

ps. 由於檔案是設定直接上傳到 s3 因此需要在本地設定環境變數 （例如 ~/.bashrc 或 ~/.bash_profile），需執行 source ~/.bashrc 才會生效

```bash
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
```

以下是一個使用 AWS EC2 和 Nginx 來部署此 API 的範例：

### 部署到雲端

要將此 API 部署到雲端，您需要選擇一個雲服務供應商，如 AWS、Google Cloud 或 Azure。以下是一個使用 AWS 的範例：

1. 在 AWS 管理控制台中，創建一個新的 EC2 實例。

2. 在 EC2 實例上安裝 Python 和必要的依賴項。

3. 將您的程式碼上傳到 EC2 實例。

4. 在 EC2 實例上，安裝並設定 Nginx。您可以使用以下命令來安裝 Nginx：

```bash
sudo apt update
sudo apt install nginx
```

5. 建立一個新的 Nginx 配置檔案，例如 `/etc/nginx/sites-available/book_crawler`，並加入以下內容：

```nginx
server {
    listen 80;
    server_name your_server_ip;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

請將 `your_server_ip` 替換為您的 EC2 實例的公開 IP 地址。

6. 建立一個指向新配置檔案的符號連結：

```bash
sudo ln -s /etc/nginx/sites-available/book_crawler /etc/nginx/sites-enabled/
```

7. 重新啟動 Nginx 以應用新的配置：

```bash
sudo service nginx restart
```

8. 在 EC2 實例上，運行以下命令來啟動 API：

```bash
python book_crawler_with_log.py
```

或者是建立一個檔案

chmod +x book_crawler_with_log.py

```ini
#!/bin/bash
python book_crawler_with_log.py 
```

```bash
nohup ./book_crawler_with_log.py &
```

如果您希望在系統開機後自動執行您的 Python 程式，您可以將它設定為系統服務。在 Linux 系統中，您可以使用 systemd 來管理系統服務。以下是如何設定的步驟：

1. 建立一個新的 systemd 服務檔案。您可以在 `/etc/systemd/system/` 目錄下建立一個新的檔案，例如 `book_crawler.service`，並加入以下內容：

```ini
[Unit]
Description=Book Crawler Service

[Service]
ExecStart=/usr/bin/python3 /path/to/your/book_crawler_with_log.py
Restart=always
User=yourusername
Group=yourgroup
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

請將 `/path/to/your/book_crawler_with_log.py` 替換為您的 Python 程式的實際路徑，並將 `yourusername` 和 `yourgroup` 替換為您的使用者名稱和群組名稱。

2. 重新載入 systemd 的配置：

```bash
sudo systemctl daemon-reload
```

3. 啟動您的服務：

```bash
sudo systemctl start book_crawler.service
```

4. 檢查您的服務是否正在運行：

```bash
sudo systemctl status book_crawler.service
```

5. 如果一切正常，您可以設定您的服務在開機時自動啟動：

```bash
sudo systemctl enable book_crawler.service
```

請注意，這只是一個基本的 systemd 服務配置。在實際配置時，您可能需要根據您的需求進行調整。例如，如果您的程式需要訪問網路，您可能需要在 `[Unit]` 部分加入 `After=network.target`。
# 使用官方 Python 執行環境作為基底映像檔
FROM python:3.12

# 複製當前目錄下的所有檔案到容器的 /app 目錄
COPY . /app

# 設定工作目錄為 /app
WORKDIR /app

# 安裝在 requirements.txt 內列出的所有 Python 套件
RUN pip3 install --no-cache-dir -r requirements.txt

# 設定 Flask 應用的位置
ENV FLASK_APP=flask_api:app

# 啟動應用程式
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
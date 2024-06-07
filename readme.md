
# Book Crawler

這是一個用於爬取書籍資訊的 Python 程式。

使用 python 3.12 版本

針對所有書籍的爬蟲網址為：https://www.books.com.tw/products/{博客來網址編號}

博客來網址編號:共 10 碼 0010000001 為起始值

針對搜尋書籍的爬蟲網址為：https://search.books.com.tw/search/query/key/{要搜尋的關鍵字}

# 安裝方式

1. cp .env.example .env
2. 修改 .env 檔案內容
3. docker-compose down && docker-compose build && docker-compose up -d 

# 如何測試 API 可以正常運作

### 測試 API

#### 使用產品編號爬取書籍資訊
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://www.books.com.tw/products/0010000009"}' http://127.0.0.1:5005/crawler-book-by-product-number
```
#### 使用搜尋 isbn 方式取得書籍資訊
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://search.books.com.tw/search/query/key/9789865069100"}' http://127.0.0.1:5005/crawler-search-book
```
#### 搜尋 ISBN 下載圖片
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://search.books.com.tw/search/query/key/9789865069100"}' http://127.0.0.1:5005/crawler-download-book-image
```


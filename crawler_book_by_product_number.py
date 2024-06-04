import requests

import time
from urllib.parse import urlparse
import os

from concurrent.futures import ThreadPoolExecutor

import concurrent.futures

# from flask import Flask, jsonify, request
import crawler_tools
from crawler_tools import timestamp

# app = Flask(__name__)
#
# @app.route('/crawl', methods=['POST'])
# def crawl():
#     url = request.json.get('url')
#     if not url:
#         return jsonify({'error': 'URL is required'}), 400
#
#     book_info = crawl_book_info(url)
#     return jsonify(book_info)

def crawl_book_info(url):
    book_info = {}  # 建立一個空字典來儲存書的資訊

    path = urlparse(url).path
    filename = os.path.basename(path)
    # Create the required directories
    crawler_tools.create_directory(timestamp)
    crawler_tools.create_directory(os.path.join(timestamp, 'logs'))
    crawler_tools.create_directory(os.path.join(timestamp, 'htmls'))
    crawler_tools.create_directory(os.path.join(timestamp, 'images'))

    soup = crawler_tools.get_page_content(url)  # Pass the logger instance as an argument
    if soup is not None:
        filename = f"output_{filename}.html"
        # 將 soup 寫入檔案
        crawler_tools.write_soup_to_file(soup, filename)  # Pass the logger instance as an argument

        # 解析資料
        book_info = crawler_tools.extract_book_info(url, soup)

        # 下載圖片
        img_url = book_info.get('圖片')
        if img_url:
            img_filename = f"download_{filename.split('.')[0]}.jpg"
            crawler_tools.download_image(img_url, img_filename)  # Pass the logger instance as an argument

    return book_info

def main():
    book_data = []  # 建立一個空列表來儲存每本書的資訊

    with requests.Session() as session:
        # 有發現有多執行序去跑被阻擋機率會提高不少，因此設定 1
        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = []
            for i in range(10000001, 10000010):
                url = f"https://www.books.com.tw/products/{str(i).zfill(10)}"
                futures.append(executor.submit(crawl_book_info, url))
                time.sleep(0.5)  # 暫停 0.5 秒

            for future in concurrent.futures.as_completed(futures):
                book_info = future.result()
                if book_info:
                    book_data.append(book_info)

    crawler_tools.export_excel(book_data)

# if __name__ == "__main__":
#
#     monitor = crawler_tools.PerformanceMonitor()
#     monitor.start()
#
#     mode = input("Enter 'api' to run as API, or 'local' to run locally: ")
#     if mode == 'api':
#         # app.run(debug=True)
#         app.run(use_reloader=False)
#     elif mode == 'local':
#         main()
#     else:
#         print("Invalid mode. Please enter 'api' or 'local'.")
#
#     monitor.stop()
#     monitor.report()

import requests
from bs4 import BeautifulSoup

import crawler_tools
from crawler_tools import timestamp

from urllib.parse import urlparse
import os

import re

from flask import Flask, jsonify, request
#
# app = Flask(__name__)
#
# @app.route('/search', methods=['POST'])
def crawl():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    book_info = crawl_search_book_info(url)
    return jsonify(book_info)
def crawl_search_book_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        return find_cheapest_book(soup)

        # 將 soup 寫入檔案
        # crawler_tools.write_soup_to_file(soup, 'output.html')
    else:
        print(f"Failed to get page content: {url}")
        return None

def find_cheapest_book(soup):
    book_info = []  # 建立一個空字典來儲存書的資訊
    books = soup.find_all('div', class_='table-td')

    min_price = float('inf')
    cheapest_book_url = None

    for book in books:
        type_elem = book.find('p')
        if type_elem and '中文書' in type_elem.text:
            price_elem = book.find('ul', class_='price clearfix')
            if price_elem:
                price = price_elem.find('b')
                if price:
                    price = int(price.text.replace(',', ''))
                    if price < min_price:
                        min_price = price
                        url_elem = book.find('a')
                        if url_elem:
                            cheapest_book_url = url_elem['href']

    if cheapest_book_url:
        cheapest_book_url = 'https:' + cheapest_book_url
        # print(cheapest_book_url)
        book_data = crawl_book_info(cheapest_book_url)
        book_info.append(book_data)

        crawler_tools.export_excel([book_data])

    return book_info

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

        # 解析資料
        book_info = crawler_tools.extract_book_info(url, soup)
        filename = book_info.get('ISBN/ISSN')
        filename = f"output_{filename}.html"
        # 將 soup 寫入檔案
        crawler_tools.write_soup_to_file(soup, filename)  # Pass the logger instance as an argument

        # 下載圖片
        img_url = book_info.get('圖片')
        if img_url:
            img_filename = f"download_{filename.split('.')[0]}.jpg"
            crawler_tools.download_image(img_url, img_filename)  # Pass the logger instance as an argument

    return book_info


def is_valid_isbn(isbn: str) -> bool:
    """Check if the input string is a valid ISBN number."""
    isbn_10_pattern = r"^(?:\d[- ]*){9}[\dxX]$"
    isbn_13_pattern = r"^(?:\d[- ]*){13}$"

    return bool(re.match(isbn_10_pattern, isbn) or re.match(isbn_13_pattern, isbn))

# if __name__ == "__main__":
#
#     # url = "https://search.books.com.tw/search/query/key/9789865069100"
#     # url = f"https://search.books.com.tw/search/query/key/{isbn}"
#
#     mode = input("Enter 'api' to run as API, or 'local' to run locally: ")
#     if mode == 'api':
#         app.run(use_reloader=False)
#     elif mode == 'local':
#         url = input("Please enter the URL: ")
#         if not url:
#             print("URL is required.")
#             exit()
#
#         monitor = crawler_tools.PerformanceMonitor()
#         monitor.start()
#
#         crawl_search_book_info(url)
#
#         monitor.stop()
#         monitor.report()
#     else:
#         print("Invalid mode. Please enter 'api' or 'local'.")
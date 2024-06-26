from . import crawler_search_book
from . import crawler_book_by_product_number
from . import crawler_download_book_image

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/crawler-download-book-image', methods=['POST'], endpoint='crawlerDownloadBookImage')
def crawlerDownloadBookImage():
    # curl -X POST -H "Content-Type: application/json" -d '{"url":"https://search.books.com.tw/search/query/key/9789865069100"}' http://127.0.0.1:5000/crawler-download-book-image-by-isbn
    url = request.json.get('url')
    print('searchCrawl', url)

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    book_info = crawler_download_book_image.crawl_search_book_info(url)
    return jsonify(book_info)

@app.route('/crawler-search-book', methods=['POST'], endpoint='crawlerSearchBook')
def crawlerSearchBook():
    # curl -X POST -H "Content-Type: application/json" -d '{"url":"https://search.books.com.tw/search/query/key/9789865069100"}' http://127.0.0.1:5000/crawler-search-book-by-isbn
    url = request.json.get('url')
    print('searchCrawl', url)

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    book_info = crawler_search_book.crawl_search_book_info(url)
    return jsonify(book_info)

@app.route('/crawler-book-by-product-number', methods=['POST'], endpoint='crawlerBookByProductNumber')
def crawlerBookByProductNumber():
    # curl -X POST -H "Content-Type: application/json" -d '{"url":"https://www.books.com.tw/products/0010000009"}' http://127.0.0.1:5000/crawler-book-by-product-number
    url = request.json.get('url')
    print('crawl', url)

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    book_info = crawler_book_by_product_number.crawl_book_info(url)
    return jsonify(book_info)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

# 這邊是方便本地測試用而留下來的

# if __name__ == "__main__":
#     app.run(use_reloader=False)

# if __name__ == "__main__":
#
#     # url = "https://search.books.com.tw/search/query/key/9789865069100"
#     # url = f"https://search.books.com.tw/search/query/key/{isbn}"
#
#     mode = input("Enter 'api' to run as API, or 'local-crawl', or 'local-crawl' to run locally: ")
#     if mode == 'api':
#         app.run(use_reloader=False)
#     elif mode == 'local-search':
#         url = input("Please enter the URL: ")
#         if not url:
#             print("URL is required.")
#             exit()
#
#         monitor = crawler_tools.PerformanceMonitor()
#         monitor.start()
#
#         crawler_search_book.crawl_search_book_info(url)
#
#         monitor.stop()
#         monitor.report()
#     elif mode == 'local-crawl':
#         monitor = crawler_tools.PerformanceMonitor()
#         monitor.start()
#
#         crawler_book_by_product_number.main()
#
#         monitor.stop()
#         monitor.report()
#     else:
#         print("Invalid mode. Please enter 'api' or 'local'.")
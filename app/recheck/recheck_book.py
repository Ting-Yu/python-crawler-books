import models.publisher as publisher_model
import models.book as book_model
import models.sqlalchemy_config as sqlalchemy_config
import models.supplier as supplier_model
import requests
from itertools import cycle
import time
import os
import json


def crawler_book(isbn):
    # Create a session object
    session = requests.Session()
    urls = [
        "https://40cpahj6c9.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
        "https://dv9reei6e1.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
        "https://9yapqipth1.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
        "https://t1gfimphld.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
        "https://sa0i2knse6.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
        "https://7h05myr281.execute-api.ap-northeast-1.amazonaws.com/production/search_book"
    ]
    url_iterator = cycle(urls)

    time.sleep(3)

    # Define the API endpoint and payload
    api_key = os.getenv('FRIBOOKER_X_API_KEY')
    url = next(url_iterator)
    print(f"API URL: {url}")
    headers = {
        'x-api-key': api_key
    }
    payload = {
        "url": "https://search.books.com.tw/search/query/key/" + isbn
    }
    response = session.post(url, json=payload, headers=headers, timeout=5)
    if response.status_code == 200:
        try:
            data = response.json()
            result = data.get('result', '')

            nested_data = json.loads(result)
            # 提取書籍資訊
            book_info = nested_data.get('book_info', {})
            # print(book_info)

            url = book_info.get('網址')
            publisher_name = book_info.get('出版社名稱')
            price = book_info.get('定價')
            print(f"URL: {url} | Publisher Name: {publisher_name} | Price: {price}")
            input("Press Enter to continue...")

        except Exception as e:
            print(f"Exception Error: {e}")

    else:
        print(f"Failed to fetch data: {response.status_code}")


def recheck_book():
    db = sqlalchemy_config.get_db()

    publishers = publisher_model.get_all_publishers(db, [], skip=0, limit=10000)
    # print(f"*** Total Publishers: {len(publishers)}")
    publisher_dict = {publisher.publisher_id: publisher for publisher in publishers}
    # print(f"*** Publisher Dict: {publisher_dict}")
    supplier = supplier_model.get_all_suppliers(db, [], skip=0, limit=10000)
    # print(f"*** Total Suppliers: {len(supplier)}")
    supplier_dict = {supplier.supplier_id: supplier for supplier in supplier}
    # print(f"*** Supplier Dict: {supplier_dict}")
    # input("Press Enter to continue...")

    page = 1
    page_size = 100
    while True:
        books = book_model.get_paginated_books(db, [
            # book_model.Book.sale_discount == 0,
            # book_model.Book.purchase_discount == 0,
        ], page=page, page_size=page_size).items
        print(f"*** Page: {page} | Page Size: {page_size} | Total Books: {len(books)}")
        # input("Press Enter to continue...")
        if len(books) == 0:
            break

        updates = []
        for book in books:
            book_id = book.book_id
            isbn = book.isbn
            ori_can_refund = book.can_refund
            # crawler_data = crawler_book(isbn)
            publisher_id = book.publisher_id
            if publisher_id in publisher_dict:
                # 同步出版社的折扣
                # sale_discount = publisher_dict[publisher_id].sale_discount
                # purchase_discount = publisher_dict[publisher_id].purchase_discount
                # updates.append({
                #     "book_id": book_id,
                #     "sale_discount": sale_discount,
                #     "purchase_discount": purchase_discount,
                # })

                # 同步供應商的退貨
                supplier_id = publisher_dict[publisher_id].supplier_id
                if supplier_id in supplier_dict:
                    supplier = supplier_dict[supplier_id]
                    return_goods = supplier.return_goods
                    updates.append({
                        "book_id": book_id,
                        "can_refund": return_goods,
                    })
                    # print(
                    #     f"Book ID: {book_id} | Publisher ID: {publisher_id} | Ori Can Refund: {ori_can_refund} Return Goods: {return_goods}")

        if updates:
            print(f"Updating {len(updates)} books...")
            print(f"Chunk All Book Ids: {', '.join(str(book['book_id']) for book in updates)}")
            # print(f"Chunk All Book Sale Discount: {', '.join(str(book['sale_discount']) for book in updates)}")
            # print(f"Chunk All Book Purchase Discount: {', '.join(str(book['purchase_discount']) for book in updates)}")
            print("----------------")
            # input("Press Enter to continue...")
            book_model.update_books_in_chunks(db, updates)

        page += 1

    db.close()


if __name__ == '__main__':
    recheck_book()

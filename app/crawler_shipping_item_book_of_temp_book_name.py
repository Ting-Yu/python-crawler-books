import os

import re
import time

import recheck.models.book as book_model
import recheck.models.shipping_item as shipping_item_model
import recheck.models.publisher as publisher_model
import recheck.models.sqlalchemy_config as sqlalchemy_config
import requests
from requests.exceptions import RequestException, Timeout
from itertools import cycle
import concurrent.futures
import json
import csv
import random
from itertools import cycle
import crawler_tools
from crawler_tools import timestamp
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def save_publish_name_to_csv(publish_name):
    with open('unfound_publishers.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([publish_name])


def extract_id_from_url(url):
    # 使用正則表達式匹配編號
    try:
        match = re.search(r'/item/(\d+)/', url)
        if match:
            return match.group(1)  # 返回匹配的第一組，即編號
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def recheck_shipping_item_book():
    db = sqlalchemy_config.get_db()
    page = 1
    page_size = 100

    while True:
        shipping_items = shipping_item_model.get_paginated_shippings(db, [
            shipping_item_model.ShippingItem.book_id.is_(None),
            shipping_item_model.ShippingItem.temp_book_name.is_not(None)
        ], page=page, page_size=page_size, sort_by=[(shipping_item_model.ShippingItem.temp_book_name, 'asc')])
        print(f"Page: {page} Page Size: {page_size}")
        if not shipping_items:
            break
        for item in shipping_items.items:
            book = book_model.get_book_by_titles(db, [item.temp_book_name])
            if len(book) > 1:
                print(f"Book Found: {book[0].title} for Shipping Item Id: {item.id} , Count {len(book)}")
                break
            elif len(book) == 1:
                print(f"Book Found: {book[0].title} for Shipping Item Id: {item.id} , Count {len(book)}")
            else:
                # print(f"{book}")
                print(f"Book Not Found for Shipping Item Id: {item.id} , Book Name: {item.temp_book_name}")

                crawler_tools.time.sleep(3)
                temp_isbn = item.temp_isbn
                temp_book_name = item.temp_book_name

                url = "https://search.books.com.tw/search/query/key/" + temp_book_name
                try:
                    book_info = {}
                    book_info = crawl_search_book_info(url)

                    if book_info is None:
                        print(f"Failed to get book information for Book Name {temp_book_name}. URL: {url}")
                        continue  # Skip to the next iteration

                    none_count = sum(value is None for value in book_info.values())

                    # Exit the function if there are 5 or more None values
                    if none_count >= 8:
                        print(f"*****Insufficient book information. Exiting function. {temp_book_name} , url =>> {url}")
                        # input(f"{book_info}")
                    else:
                        print(f"Book Info: {book_info}")
                        # input("*****Press Enter to continue...")
                        modify_data(book_info, db, temp_book_name)

                    # input("Press Enter to continue...")
                    # response = session.post(url, json=payload, headers=headers, timeout=5)
                    # print(f"Temp Book Name: {temp_book_name}")
                    # if response.status_code == 200:
                    #     try:
                    #         data = response.json()
                    #         modify_data(data, db, temp_isbn)
                    #
                    #
                    #     except Exception as e:
                    #         print(f"Exception Error: {e}")
                    #
                    # else:
                    #     print(f"Failed to fetch data: {response.status_code} message: {response.text}")

                except (RequestException, Timeout) as e:
                    print(f"Request failed: {e}")

        page += 1

    db.close()


def modify_data(book_info, db, temp_book_name):
    url = book_info.get('網址')
    book_crawler_id = extract_id_from_url(url)
    category = book_info.get('商品類別')
    title = book_info.get('中文書名')
    origin_title = book_info.get('原文書名')
    book_number = book_info.get('書號')
    publisher_name = book_info.get('出版社名稱')
    published_at = book_info.get('出版日期')
    author = book_info.get('作者中文名')
    author_foreign = book_info.get('作者外文名')
    translator = book_info.get('譯者')
    isbn = book_info.get('ISBN/ISSN')
    price = book_info.get('定價')
    china_book_classification_number = book_info.get('中國圖書分類號')
    open_number = book_info.get('開數')
    binding = book_info.get('平/精裝')
    pages = book_info.get('頁數')
    edition = book_info.get('版次')
    level = book_info.get('級別')
    printing = book_info.get('印刷')
    publish_place = book_info.get('Publish Place')
    img_url = book_info.get('圖片')
    author_intro = book_info.get('作者簡介')
    content_intro = book_info.get('內容簡介')
    agenda = book_info.get('目錄')
    award = book_info.get('得獎與推薦紀錄')
    event = book_info.get('重要事件')

    # pages_numbers_only = re.findall(r'\d+', pages)
    #
    # # Convert the extracted numbers to a single integer, assuming the first match is the desired one
    # pages = int(pages_numbers_only[0]) if pages_numbers_only else 0

    print(f"Book Crawler ID: {book_crawler_id}")
    # print(f"Category: {category}")
    # print(f"Title: {title}")
    # print(f"Origin Title: {origin_title}")
    # print(f"Book Number: {book_number}")
    # print(f"Publish Name: {publisher_name}")
    # print(f"Publish Date: {published_at}")
    # print(f"Author: {author}")
    # print(f"Author Foreign: {author_foreign}")
    # print(f"Translator: {translator}")
    # print(f"ISBN: {isbn}")
    # print(f"Price: {price}")
    # print(f"China Book Classification Number: {china_book_classification_number}")
    # print(f"Open Number: {open_number}")
    # print(f"Binding: {binding}")
    # print(f"Pages: {pages}")
    # print(f"Edition: {edition}")
    # print(f"Level: {level}")
    # print(f"Printing: {printing}")
    # print(f"Publish Place: {publish_place}")
    # print(f"Image URL: {img_url}")
    # print(f"Author Intro: {author_intro}")
    # print(f"Content Intro: {content_intro}")
    # print(f"Agenda: {agenda}")
    # print(f"Award: {award}")
    # print(f"Event: {event}")

    publisher_name = crawler_tools.map_publisher_name(publisher_name)
    publisher = publisher_model.get_publisher_by_name(db, publisher_name)
    if publisher:
        print(f"Publisher ID: {publisher.publisher_id} of {publisher.name}")
        publisher_id = publisher.publisher_id
        sale_discount = publisher.sale_discount
        purchase_discount = publisher.purchase_discount
        upsert_data = {
            'book_crawler_id': book_crawler_id,
            'isbn': isbn,
            'title': title,
            'publisher_id': publisher_id,
            'published_at': published_at,
            'author': author,
            'translator': translator,
            'cover': img_url,
            'price': price,
            'description': content_intro,
            'author_intro': author_intro,
            'origin_title': origin_title,
            'author_foreign': author_foreign,
            'open_number': open_number,
            'soft_hard_cover': binding,
            'page_count': pages,
            'edition': edition,
            'important_event': event,
            'book_number': book_number,
            'publisher_name': publisher_name,
            'catalog': agenda,
            'reward_history': award,
            'china_book_class': china_book_classification_number,
            'tax': '免稅',
            'sale_discount': sale_discount,
            'purchase_discount': purchase_discount,
            'stock': 0,
            'status': 1,
            'book_type': 1,
            'can_refund': 0,
            'limit_count': 0,
        }


        book_model.upsert_book(db, upsert_data)
        book = book_model.get_book_by_isbn(db, isbn)

        if book:
            print(f"Book ID: {book.book_id} of {book.title}")
            shipping_item_model.update_shipping_item_by_temp_book_name(db, temp_book_name, {'book_id': book.book_id, 'isbn': isbn})
            print(f"-----")
            # input("Press Enter to continue...")
    else:
        save_publish_name_to_csv(publisher_name)
        print(f"Publisher {publisher_name} not found")
        print(f"-----")

    #### 會寫入
    # isbn = Column(String(255), nullable=True, comment='ISBN')
    # title = Column(String(255), nullable=False, comment='書名')
    # publisher_id = Column(BigInteger, ForeignKey('publishers.publisher_id'), nullable=False,
    #                       comment='出版社編號')
    # published_at = Column(Date, nullable=True, comment='出版日期')
    # author = Column(String(255), nullable=False, comment='作者')
    # translator = Column(String(255), nullable=True, comment='譯者')
    # cover = Column(String(255), nullable=True, comment='封面')
    # price = Column(Integer, nullable=False, comment='定價')
    # description = Column(Text, nullable=True, comment='內容簡介')
    # author_intro = Column(Text, nullable=True, comment='作者簡介')
    # origin_title = Column(String(255), nullable=True, comment='原文書名')
    # author_foreign = Column(String(255), nullable=True, comment='作者外文名')
    # open_number = Column(String(255), nullable=True, comment='開數')
    # page_count = Column(Integer, nullable=False, default=0, comment='頁數')
    # edition = Column(String(255), nullable=True, comment='版次')
    # soft_hard_cover = Column(String(255), nullable=True, comment='平/精裝')
    # catalog = Column(Text, nullable=True, comment='目錄')
    # important_event = Column(Text, nullable=True, comment='重要事件')
    # reward_history = Column(Text, nullable=True, comment='得獎與推薦紀錄')
    # china_book_class = Column(String(255), nullable=True, comment='中國圖書分類號')

    #### 找不到
    # book_id = Column(BigInteger, primary_key=True, autoincrement=True)
    # book_crawler_id = Column(String(255), nullable=True)
    # tax = Column(String(255), nullable=False, comment='稅別')
    # sale_discount = Column(DECIMAL(10, 2), nullable=False)
    # purchase_discount = Column(DECIMAL(10, 2), nullable=False)
    # created_at = Column(DateTime, nullable=True, default=func.now())
    # updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    # stock = Column(Integer, nullable=False, default=0)
    # status = Column(Integer, nullable=False, default=1, comment='書籍狀態')
    # barcode = Column(String(255), nullable=True, comment='條碼')
    # book_number = Column(String(255), nullable=True, comment='書號')
    # book_type = Column(Integer, nullable=False, default=1, comment='商品類別')
    # can_refund = Column(Integer, nullable=False, default=0, comment='可否退書')
    # limit_count = Column(Integer, nullable=False, default=0, comment='限定本數')
    # online_date = Column(Date, nullable=True, comment='上架日期')
    # project_intro = Column(Text, nullable=True, comment='專案簡介')
    # publisher_name = Column(String(255), nullable=True)


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
    book_info = {}
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
        book_info = book_data

    return book_info


def crawl_book_info(url):
    book_info = {}  # 建立一個空字典來儲存書的資訊

    path = urlparse(url).path
    time.sleep(3)
    soup = crawler_tools.get_page_content(url)  # Pass the logger instance as an argument
    if soup is not None:
        # 解析資料
        book_info = crawler_tools.extract_book_info(url, soup)

    return book_info


if __name__ == "__main__":
    # print("Start rechecking shipping items")
    recheck_shipping_item_book()

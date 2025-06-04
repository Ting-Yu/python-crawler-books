import models.publisher as publisher_model
import models.book as book_model
import models.sqlalchemy_config as sqlalchemy_config
import models.supplier as supplier_model
import requests
from itertools import cycle
import time
import os
import json
import re

urls = [
    "https://40cpahj6c9.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
    "https://8bzeo1ztf8.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
    "https://kksbry3653.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
    "https://nkcxbc5wzc.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
    "https://dv9reei6e1.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
    "https://9yapqipth1.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
    "https://t1gfimphld.execute-api.ap-northeast-1.amazonaws.com/production/search_book"
]
url_iterator = cycle(urls)


def crawler_book(db,isbn):

    exist_book = book_model.first_book_by_isbn(db,isbn)
    if exist_book:
        print(f"Book Exist: {isbn}")
        return
    else:
        print(f"Book Not Exist: {isbn}")
        # Create a session object
        session = requests.Session()

        time.sleep(120)

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
        response = session.post(url, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            try:
                data = response.json()
                result = data.get('result', '')

                nested_data = json.loads(result)
                # 提取書籍資訊
                book_info = nested_data.get('book_info', {})
                # print(book_info)
                return book_info

            except Exception as e:
                print(f"Exception Error: {e}")

        else:
            print(f"Failed to fetch data: {response.status_code}")


def recheck_book():
    db = sqlalchemy_config.get_db()

    publishers = publisher_model.get_all_publishers(db, [], skip=0, limit=10000)
    # print(f"*** Total Publishers: {len(publishers)}")
    publisher_dict = {publisher.publisher_id: publisher for publisher in publishers}
    publisher_dict_name = {publisher.name: publisher for publisher in publishers}
    # print(f"*** Publisher Dict: {publisher_dict}")
    supplier = supplier_model.get_all_suppliers(db, [], skip=0, limit=10000)
    # print(f"*** Total Suppliers: {len(supplier)}")
    supplier_dict = {supplier.supplier_id: supplier for supplier in supplier}
    # print(f"*** Supplier Dict: {supplier_dict}")
    # input("Press Enter to continue...")

    books = [
        "9786269679287",
        "9786269863006",
        "9789863429654",
        "9789576582257",
        "4711132385212",
        "9786263773462",
        "9786267174609",
        "9786263749269",
        "9786267352373",
        "9786267281796",
        "9789862943106",
        "4711132384772",
        "9786269796793",
        "9786263748491",
        "9786269720651",
        "9789860409611",
        "9786269827176",
        "9789570535709",
        "2284597660382",
        "9789861798783",
        "9786263207592",
        "9789864899388",
        "9786263771079",
        "9786263771086",
        "9786263771093",
        "9786267339602",
        "9786263058811",
        "9786263058828",
        "9789869472241",
        "4717702296025",
        "9786263582347",
        "9789865248628",
        "9786263266551",
        "9789577519474",
        "4717211036488",
        "9786263791824",
        "4717702123864",
        "9789861798387",
        "9786263057029",
        "9786263208087",
        "9786267284445",
        "8667106517447",
        "9786267193631",
        "9786267193662",
        "9786263778955",
        "9786267366325",
        "9789573614340",
        "9786269798322",
        "9789863127734",
        "9786263962453",
        "9789861786957",
        "9786267368213",
        "4717702122737",
        "9789865329495",
        "9786263701625",
        "9789864004935",
        "9786267074893",
        "9786267405666",
        "9789575217013",
        "9786263583979",
        "9786263583276",
        "9786269818709",
        "9786263733725",
        "9786267333259",
        "9786267336731",
        "9786269827145",
        "9789869222860",
        "9786269649297",
        "9789861305806",
        "4711228581788",
        "4711228581795",
        "4711228582884",
        "4711228581283",
        "4711228581290",
        "4711228584314",
        "9786263204836",
        "9786267000373",
        "9786267197387",
        "9786263527867",
        "9786263783843",
        "9786263227835",
        "9789887416272",
        "9786263245501",
        "9789861617411",
        "9786263748286",
        "9780020240426",
        "9786267405659",
        "9786269565825",
        "9786267367131",
        "9786263207424",
        "9786263207455",
        "9789864524426",
        "9786267271537",
        "9786269606450",
        "9789860691788",
        "9786269827206",
        "9786267367278",
        "9786267279687",
        "9789863877264",
        "9786263496538",
        "9789865069865",
        "9789865069513",
        "9786263208612",
        "9786267365687",
        "9789864524822",
        "9789864524815",
        "9786260118167",
        "9789575034481",
        "9786267329849",
        "9786263791794",
        "9786267328125",
        "9786263840676",
        "9786263582972",
        "9786263770041",
        "9786263770966",
        "9786263772311",
        "9786263773813",
        "9786263775374",
        "9786269832538",
        "9786263775299",
        "9786263775282",
        "9789863706854",
        "9786263901605",
        "9786263208186",
        "9786267307021",
        "9786263558113",
        "9789861798851",
        "9786263145733",
        "9786267207659",
        "9789571475462",
        "9786267346808",
        "9786267346792",
        "9786269757152",
        "9786263583351",
        "9786267427514",
        "9786267212899",
        "9786267427774",
        "9786263772199",
        "9789860697247",
        "9789570850253",
        "9789868343375",
        "9786267441282",
        "9786267441220",
        "9786267381281",
        "9786269642564",
        "9786269603275",
        "9789571477848",
        "9786263208551",
        "9789571199238",
        "9789577276346",
        "9786267279748",
        "9786263722996",
        "9786263557567",
        "9786263557550",
        "4713302431552",
        "9786267448229",
        "9786267448236",
        "9786267284537",
        "9786267182840",
        "9786267127445",
        "9786267350911",
        "9786267428689",
        "9786267401132",
        "9789864899500",
        "4717702295998",
        "9786263431799",
        "9789863779742",
        "9789863779735",
        "9789869428866",
        "9786260213343",
        "9786269765973",
        "9786269748068",
        "9786269792238",
        "9786263146310",
        "9786263777262",
        "9786263962286",
        "9786263106741",
        "9786269820276",
        "9789570535716",
        "9786269801589",
        "9786267401453",
        "9786263434400",
        "9786267372470",
        "9786263791749",
        "9786267304457",
        "9789861344928",
        "9786267394809",
        "4717702296476",
        "9786267345283",
        "9786263950092",
        "9786267291924",
        "9786267195666",
        "9789865470906",
        "9786263154162",
        "9786269672288",
        "9789860507270",
        "9786267250921",
        "9789579014939",
        "9789571477527",
        "9786267415078",
        "4711099771837",
        "9786269507344",
        "9786269796908",
        "9786269842285",
        "9786263495517",
        "9786263980198",
        "2284597660429",
        "9789887007524",
        "9786269559428",
        "9786263781764",
        "9786269572878",
        "9789572683439",
        "9789572691137",
        "9786263791602",
        "9786263744516",
        "9786263748040",
        "9789861787220",
        "9786263206649",
        "9786267394564",
        "9786269611867",
        "9786269801862",
        "9786263728295",
        "9786263298231",
        "9786267474235",
        "9786267474242",
        "4711441071189",
        "9786269754694"
    ]

    updates = []
    for book in books:
        print(f"*** Checking Book: {book} ***")

        crawler_data = crawler_book(db,book)
        if crawler_data:
            url = crawler_data.get('網址')
            book_crawler_id = extract_id_from_url(url)
            category = crawler_data.get('商品類別')
            title = crawler_data.get('中文書名')
            origin_title = crawler_data.get('原文書名')
            book_number = crawler_data.get('書號')
            publisher_name = crawler_data.get('出版社名稱')
            published_at = crawler_data.get('出版日期')
            author = crawler_data.get('作者中文名')
            author_foreign = crawler_data.get('作者外文名')
            translator = crawler_data.get('譯者')
            isbn = crawler_data.get('ISBNISSN')
            price = crawler_data.get('定價')
            china_book_classification_number = crawler_data.get('中國圖書分類號')
            open_number = crawler_data.get('開數')
            binding = crawler_data.get('平/精裝')
            pages = crawler_data.get('頁數')
            edition = crawler_data.get('版次')
            level = crawler_data.get('級別')
            printing = crawler_data.get('印刷')
            publish_place = crawler_data.get('Publish Place')
            img_url = crawler_data.get('圖片')
            author_intro = crawler_data.get('作者簡介')
            content_intro = crawler_data.get('內容簡介')
            agenda = crawler_data.get('目錄')
            award = crawler_data.get('得獎與推薦紀錄')
            event = crawler_data.get('重要事件')

            if publisher_name not in publisher_dict_name:
                publisher_id = 9999
                sale_discount = 0.7
                purchase_discount = 0.6
            else:
                publisher_id = publisher_dict_name[publisher_name].publisher_id
                sale_discount = publisher_dict_name[publisher_name].sale_discount
                purchase_discount = publisher_dict_name[publisher_name].purchase_discount

            # print(f"ISBN: {isbn} | Crawler Data: {crawler_data}")
            modify_data = {
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
                'sale_discount': sale_discount,
                'purchase_discount': purchase_discount,
                'tax': '免稅',
                'stock': 0,
                'status': 1,
                'book_type': 1,
                'can_refund': 0,
                'limit_count': 0,
            }
            result = book_model.upsert_book(db, modify_data)
            print(f"*** Book Updated: {isbn} | {result} ***")
            # input("Press Enter to continue...")

    # if updates:
    #     print(f"Updating {len(updates)} books...")
    #     print(f"Chunk All Book Ids: {', '.join(str(book['book_id']) for book in updates)}")
    #     # print(f"Chunk All Book Sale Discount: {', '.join(str(book['sale_discount']) for book in updates)}")
    #     # print(f"Chunk All Book Purchase Discount: {', '.join(str(book['purchase_discount']) for book in updates)}")
    #     print("----------------")
    #     # input("Press Enter to continue...")
    #     book_model.update_books_in_chunks(db, updates)

    db.close()


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


if __name__ == '__main__':
    recheck_book()

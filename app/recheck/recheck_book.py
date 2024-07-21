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
    "https://dv9reei6e1.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
    "https://9yapqipth1.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
    "https://t1gfimphld.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
    "https://sa0i2knse6.execute-api.ap-northeast-1.amazonaws.com/production/search_book",
    "https://7h05myr281.execute-api.ap-northeast-1.amazonaws.com/production/search_book"
]
url_iterator = cycle(urls)


def crawler_book(isbn):
    # Create a session object
    session = requests.Session()

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

    page = 1
    page_size = 100
    while True:
        books = book_model.get_paginated_books(db, [
            # book_model.Book.book_crawler_id == 0,
            book_model.Book.publisher_id == 9999,
            book_model.Book.publisher_name != '未分類'
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
            publisher_id = book.publisher_id

            # crawler_data = crawler_book(isbn)
            # if crawler_data:
            #     url = crawler_data.get('網址')
            #     book_crawler_id = extract_id_from_url(url)
            #     category = crawler_data.get('商品類別')
            #     title = crawler_data.get('中文書名')
            #     origin_title = crawler_data.get('原文書名')
            #     book_number = crawler_data.get('書號')
            #     publisher_name = crawler_data.get('出版社名稱')
            #     published_at = crawler_data.get('出版日期')
            #     author = crawler_data.get('作者中文名')
            #     author_foreign = crawler_data.get('作者外文名')
            #     translator = crawler_data.get('譯者')
            #     isbn = crawler_data.get('ISBNISSN')
            #     price = crawler_data.get('定價')
            #     china_book_classification_number = crawler_data.get('中國圖書分類號')
            #     open_number = crawler_data.get('開數')
            #     binding = crawler_data.get('平/精裝')
            #     pages = crawler_data.get('頁數')
            #     edition = crawler_data.get('版次')
            #     level = crawler_data.get('級別')
            #     printing = crawler_data.get('印刷')
            #     publish_place = crawler_data.get('Publish Place')
            #     img_url = crawler_data.get('圖片')
            #     author_intro = crawler_data.get('作者簡介')
            #     content_intro = crawler_data.get('內容簡介')
            #     agenda = crawler_data.get('目錄')
            #     award = crawler_data.get('得獎與推薦紀錄')
            #     event = crawler_data.get('重要事件')
            #
            #     publisher_name = map_publisher_name(publisher_name)
            #     if publisher_name in publisher_dict_name:
            #         publisher_id = publisher_dict_name[publisher_name].publisher_id
            #         sale_discount = publisher_dict_name[publisher_name].sale_discount
            #         purchase_discount = publisher_dict_name[publisher_name].purchase_discount
            #
            #         print(f"Book ID: {book_id} | ISBN: {isbn} | Crawler Data: {crawler_data}")
            #         input("Press Enter to continue...")
            #         modify_data = {
            #             'book_id': book_id,
            #             'book_crawler_id': book_crawler_id,
            #             'isbn': isbn,
            #             'title': title,
            #             'publisher_id': publisher_id,
            #             'published_at': published_at,
            #             'author': author,
            #             'translator': translator,
            #             'cover': img_url,
            #             'price': price,
            #             'description': content_intro,
            #             'author_intro': author_intro,
            #             'origin_title': origin_title,
            #             'author_foreign': author_foreign,
            #             'open_number': open_number,
            #             'soft_hard_cover': binding,
            #             'page_count': pages,
            #             'edition': edition,
            #             'important_event': event,
            #             'book_number': book_number,
            #             'publisher_name': publisher_name,
            #             'catalog': agenda,
            #             'reward_history': award,
            #             'china_book_class': china_book_classification_number,
            #             'sale_discount': sale_discount,
            #             'purchase_discount': purchase_discount,
            #         }
            #         updates.append(modify_data)

            publisher_name = book.publisher_name
            publisher_name = map_publisher_name(publisher_name)
            if publisher_name in publisher_dict_name:
                publisher_id = publisher_dict_name[publisher_name].publisher_id
                sale_discount = publisher_dict_name[publisher_name].sale_discount
                purchase_discount = publisher_dict_name[publisher_name].purchase_discount
                updates.append({
                    "book_id": book_id,
                    "publisher_id": publisher_id,
                    "sale_discount": sale_discount,
                    "purchase_discount": purchase_discount,
                })

            # if publisher_id in publisher_dict:
            #     # 同步出版社的折扣
            #     # sale_discount = publisher_dict[publisher_id].sale_discount
            #     # purchase_discount = publisher_dict[publisher_id].purchase_discount
            #     # updates.append({
            #     #     "book_id": book_id,
            #     #     "sale_discount": sale_discount,
            #     #     "purchase_discount": purchase_discount,
            #     # })
            #
            #     # 同步供應商的退貨
            #     supplier_id = publisher_dict[publisher_id].supplier_id
            #     if supplier_id in supplier_dict:
            #         supplier = supplier_dict[supplier_id]
            #         return_goods = supplier.return_goods
            #         updates.append({
            #             "book_id": book_id,
            #             "can_refund": return_goods,
            #         })
            #         # print(
            #         #     f"Book ID: {book_id} | Publisher ID: {publisher_id} | Ori Can Refund: {ori_can_refund} Return Goods: {return_goods}")

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


def map_publisher_name(old_name):
    # Mapping of old publisher names to new publisher names
    publisher_name_map = {
        "大溏": "大溏文化",
        "木馬文化": "木馬",
        "時報出版": "時報文化",
        "大石國際文化": "大石",
        "衛城出版": "衛城",
        "書林出版有限公司": "書林出版",
        "尖端": "尖端(漫畫拆封不退)",
        "好讀": "好讀出版",
        "澄波藝術文化股份有限公司": "澄波藝術文化有限公司",
        "國立中央大學": "國立中央大學臺經中心",
        "青文": "青文(漫畫拆封不退)",
        "PCuSER電腦人文化": "PCUSER電腦人",
        "水牛": "水牛(集單較久)",
        "晨星": "晨星出版",
        "楓樹林出版社": "楓樹林",
        "春天出版社": "春天",
        "新經典文化": "新經典",
        "太雅出版社": "太雅出版",
        "原動力文化": "原動力",
        "東立": "東立（拆封不退）",
        "柏樂出版有限公司": "柏樂出版",
        "台灣角川": "角川(漫畫拆封不退)",
        "高寶": "高寶國際",
        "初文出版社有限公司": "初文出版社",
        "三采": "三采文化",
        "三民": "三民書局",
        "如果出版社": "如果出版",
        "健行": "健行文化",
        "大田": "大田出版",
        "香港kubrick": "KUBRICK",
        "蓋亞": "蓋亞文化",
        "方舟文化": "方舟",
        "農業部林業及自然保育署": "農業部林業及自然保育署（直往，買斷）",
        "奧林": "奧林文化",
        "主流出版社": "主流出版",
        "奇異果文創事業有限公司": "奇異果文創",
        "奇光出版": "奇光",
        "朱雀": "朱雀文化",
        "網路與書出版": "網路與書",
        "風和文創": "風和文創事業有限公司",
        "深智數位": "深智數位股份有限公司",
        "維京": "維京國際",
        "台北市政府文化局": "台北市政府文化局【買斷不退】",
        "國立陽明交通大學出版社": "陽明交通大學出版社",
        "天空數位圖書": "天空數位",
        "FormsKitchen": "Forms Kitchen",
        "ToBeCharm": "To Be Charm",
        "ZKOOBLTD.": "ZKOOB LTD.",
        "一家親": "一家親文化有限公司",
        "一起來": "一起來出版",
        "上誼": "上誼文化公司",
        "世一(僅限字典)": "世一(非所有品項皆有經銷)",
        "二魚": "二魚文化",
        "八旗": "八旗文化",
        "典絃": "典絃音樂文化國際事業",
        "城邦網路社群MyBase": "城邦網路社群My Base",
        "大塊（漫畫拆封不退）": "大塊文化",
        "大家": "大家出版",
        "大拓": "大拓文化",
        "大旗": "大旗出版社",
        "大智": "大智景R",
        "大樂": "大樂文化",
        "大牌": "大牌出版",
        "大辣（漫畫拆封不退）": "大辣",
        "大邁": "大邁文化",
        "大都會文化": "大都會文化事業有限公司",
        "天肯文化出版有限公司": "天肯文化出版有限公司（2017年7月已終止合作）",
        "小熊": "小熊森林",
        "小異": "小異出版",
        "山海文化": "山海文化雜誌社",
        "康鑑(人類文化)": "康鑑 (人類文化)",
        "書局": "三民書局",
        "東方出版": "台灣東方",
        "欣然出版社": "欣然出版社（結束代理）",
        "洪範書店": "洪範",
        "理得": "理 得",
        "皇冠文化": "皇冠",
        "經典雜誌(當期及前兩期)(與供應商結束合作)": "【結束合作】經典雜誌(當期及前兩期)(直往)",
        "聯合文學出版社": "聯合文學",
        "遠足": "遠足文化",
        "阿橋社": "阿橋社文化",
        "集合": "集合出版社",
        "龍溪": "龍溪（集單不易）",
        "國立臺灣歷史博物館()": "國立臺灣歷史博物館(三民)",
        "香港三聯(註書店調書)": "香港三聯(註書店調書用)",
        "五花鹽(集單門檻60本或5000元)": "五花鹽",
        "952vazaytamo": "952 vazay tamo",
        "AMoney優財": "A Money優財",
        "browniepublishing": "brownie publishing(2024.6起掛至紅螞蟻)",
        "（）八方文化創作室": "（三民）八方文化創作室",
        "TaiwanComix": "Taiwan Comix",
        "經典（聯合發行，僅限書籍）": "經典雜誌出版社（聯合發行，僅限書籍）",
        "經典雜誌(書籍及過刊雜誌)(與供應商結束合作)": "【結束合作】經典雜誌(過刊號及書籍)(直往)",
        "正中(應稅)": "正中【大多數應稅】",
        "Ron&MarkHanson": "Ron & Mark Hanson",
        "新BOOKHOUSE-新潮社": "新BOOK HOUSE-新潮社",
        "dirtypress": "dirty press",
        "米通信【買斷不退】": "米通信 【買斷不退】",
        "LittleBrown&Co": "Little Brown & Co",
        "獨立媒體(香港)": "獨立媒體 (香港)",
        "角頭音樂［結束合作］": "【結束合作】角頭音樂",
        "P.PLUSLIMITED": "P.PLUS LIMITED",
        "katiyani如觀": "Katiyani 如觀",
        "不然呢BrandNew青年文集": "不然呢 Brand New 青年文集",
        "甘肅少年兒童出版社（非代理，不可訂購）": "甘肅少年兒童出版社（非三民代理，不可訂購）",
        "DigitalMedicine": "digital medicine tshut-pán-siā",
        "SiuromaOfficial": "Siuroma Official",
        "RoaringBrook【原文書，買斷不退】": "Roaring Brook【原文書，買斷不退】",
        "CartwheelBooks【原文書，買斷不退】": "Cartwheel Books【原文書，買斷不退】",
        "Independentlypublished": "Independently published",
        "WowMedia": "Wow Media",
        "樂興之時管絃樂團【買斷不退】": "樂興之時管絃樂團 【買斷不退】",
        "蜂鳥（專案，不可建檔訂購）": "蜂鳥（特殊專案）",
        "UmbrellaUprising": "Umbrella Uprising",
        "sconepublishing": "scone publishing(2024.6起掛至紅螞蟻)",
        "SingLeeArt": "SingLee Art",
        "dmpeditions": "dmp editions",
        "VintageBooks【原文書，買斷不退】": "Vintage Books【原文書，買斷不退】",
        "Thames&HudsonsUK【原文書，買斷不退】": "Thames & Hudsons UK【原文書，買斷不退】",
        "LarkBooksUK【原文書，買斷不退】": "Lark Books UK【原文書，買斷不退】",
        "AtheneumBooks【原文書，買斷不退】": "Atheneum Books【原文書，買斷不退】",
        "Denzel&WittCreation【買斷不退】": "Denzel & Witt Creation【買斷不退】",
        "EachModern亞紀畫廊": "Each Modern 亞紀畫廊",
        "Baggins&Gamgee（中土世界）": "Baggins & Gamgee（中土世界）",
        "CookinnTaiwan": "Cookinn Taiwan"
    }

    if old_name in publisher_name_map:
        return publisher_name_map[old_name]
    else:
        return old_name


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

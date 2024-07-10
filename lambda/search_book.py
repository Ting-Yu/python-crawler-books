import json
import requests
from bs4 import BeautifulSoup
from botocore.exceptions import ClientError

import tools

from urllib.parse import urlparse
import os

import re
import boto3


def lambda_handler(event, context):
    try:
        # 確認 httpMethod 存在於 event 中
        method = event.get('httpMethod', 'UNKNOWN')

        # 確認 body 存在於 event 中，並解析 JSON
        body = event.get('body', '{}')
        url = ''
        result = '{}'
        if body:
            body = json.loads(body)
            url = body.get('url', 'not found')
            result = crawl_search_book_info(url)

        if method == 'POST':
            response = {
                'statusCode': 200,
                'body': f"POST request received with data: {body}",
                'url': url,
                'result': json.dumps(result)
            }
            return {
                'statusCode': 200,
                'body': json.dumps(response)
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps(f"Unsupported method: {method}")
            }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f"KeyError: {str(e)}")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal server error: {str(e)}")
        }


def crawl_search_book_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        return find_cheapest_book(soup)

        # 將 soup 寫入檔案
        # tools.write_soup_to_file(soup, 'output.html')
    else:
        # print(f"Failed to get page content: {url}")
        return None


def find_cheapest_book(soup):
    image_info = {}  # 建立一個空字典來儲存書的資訊
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
        return crawl_book_info(cheapest_book_url)

    return image_info


def crawl_book_info(url):
    image_info = {
        'statusCode': 'crawl book info default'
    }

    path = urlparse(url).path
    filename = os.path.basename(path)
    # Create the required directories
    # tools.create_directory(timestamp)
    # tools.create_directory(os.path.join(timestamp, 'logs'))
    # tools.create_directory(os.path.join(timestamp, 'htmls'))
    # tools.create_directory(os.path.join(timestamp, 'images'))
    # return {
    #     'path':path,
    #     'filename':filename,
    #     'url':url
    # }

    soup = tools.get_page_content(url)  # Pass the logger instance as an argument

    image_info = {
        'statusCode': 'crawl book info run soup'
    }

    if soup is not None:
        # filename = f"output_{filename}.html"
        # 將 soup 寫入檔案
        # tools.write_soup_to_file(soup, filename)  # Pass the logger instance as an argument

        # 解析資料
        # book_info = tools.extract_book_info(url, soup)
        book_info = extract_book_info(url, soup)

        image_info = {
            'statusCode': 'crawl book info run book_info'
        }

        # 下載圖片
        img_url = book_info.get('圖片')

        image_info = {
            'statusCode': 'crawl book info run img_url',
            'img_url': img_url
        }
        if img_url:
            filename = book_info.get('ISBNISSN')
            img_filename = f"download_{filename.split('.')[0]}.jpg"
            # img_filename = tools.download_image(img_url, img_filename)  # Pass the logger instance as an argument

            # 從 URL 下載圖片
            response = requests.get(img_url, stream=True)
            response.raise_for_status()

            # print('img_filename', img_filename)
            # s3_url = tools.upload_file_to_s3(img_filename, 'fribooker')
            s3_url = upload_file_to_s3(response.raw, 'fribooker', img_filename)
            return {
                'book_info': book_info,
                'filename': filename,
                'image_directory': img_filename,
                'image_url': img_url,
                's3_url': s3_url
            }

    return image_info


def is_valid_isbn(isbn: str) -> bool:
    """Check if the input string is a valid ISBN number."""
    isbn_10_pattern = r"^(?:\d[- ]*){9}[\dxX]$"
    isbn_13_pattern = r"^(?:\d[- ]*){13}$"

    return bool(re.match(isbn_10_pattern, isbn) or re.match(isbn_13_pattern, isbn))


def extract_book_info(url, soup):
    category_elems = soup.find_all('li', {'property': 'itemListElement'})
    category = [elem.text.strip() for elem in category_elems] if category_elems else []
    # category_name = ' '.join(category)
    category_name = ' '.join(category[:3])

    # second_category_elems = soup.find('li').find_all('a')
    # second_category = [elem.text.strip() for elem in second_category_elems] if second_category_elems else []
    # second_category_name = ' '.join(second_category)
    # print(second_category_name)

    title_div_elem = soup.find('div', {'class': 'mod type02_p002 clearfix'})
    title_elem = title_div_elem.h1 if title_div_elem and hasattr(title_div_elem, 'h1') else None
    title = title_elem.text.strip() if title_elem else None

    author_elem = soup.find('a', href=lambda x: x and 'adv_author' in x)
    author = author_elem.text.strip() if author_elem else None

    translator_elems = soup.find_all('a', href=lambda x: x and 'adv_author' in x)
    translator = translator_elems[1].text.strip() if len(translator_elems) > 1 else None

    publisher_elem = soup.find('a', href=lambda x: x and 'sys_puballb' in x)
    publisher = publisher_elem.span.text.strip() if publisher_elem and hasattr(publisher_elem, 'span') else None

    publish_date_elem = soup.find('li', string=lambda x: x and '出版日期' in x)
    publish_date = publish_date_elem.text.strip().split('：')[-1] if publish_date_elem else None

    price_elem = soup.find('ul', class_='price')
    price = price_elem.find('em').text.strip() if price_elem else None

    isbn_elem = soup.find('li', string=lambda x: x and 'ISBN' in x)
    isbn = isbn_elem.text.strip().split('：')[-1] if isbn_elem else None

    series_elem = soup.find('li', string=lambda x: x and '叢書系列' in x)
    series = series_elem.a.text.strip() if series_elem and hasattr(series_elem, 'a') else None

    # spec_elem = soup.find('li', string=lambda x: x and '規格' in x)
    # if spec_elem:
    #     spec = spec_elem.text.strip().split('：')[-1]
    #     # 使用 '/' 符號進行切割
    #     spec_parts = spec.split('/')
    #     spec = [part.strip() for part in spec_parts]
    # else:
    #     spec = []

    spec_elem = soup.find('li', string=lambda x: x and '規格' in x)
    if spec_elem:
        spec_raw = spec_elem.text.strip().split('：')[-1]  # Extract the spec string after '規格：'
        spec_parts = spec_raw.split('/')  # Split the spec string into parts using '/'
        spec = [part.strip() for part in spec_parts if part.strip()]  # Clean and filter empty parts
    else:
        spec = []  # Default to an empty list if '規格' is not found

    publish_place_elem = soup.find('li', string=lambda x: x and '出版地' in x)
    publish_place = publish_place_elem.text.strip().split('：')[-1] if publish_place_elem else None

    img_elem = soup.find('img', {'class': 'cover M201106_0_getTakelook_P00a400020052_image_wrap'})
    img_url = img_elem['src'] if img_elem else None

    # Finding "內容簡介"
    content_intro = ''
    content_intro_heading = soup.find(lambda tag: tag.name == "h3" and "內容簡介" in tag.text)
    if content_intro_heading and content_intro_heading.find_next_sibling("div"):
        content_intro = content_intro_heading.find_next_sibling("div").text.strip()
    # else:
    #     print("內容簡介 not found or has no following div.")

    # Finding "作者介紹"
    author_intro = ''
    author_intro_heading = soup.find(lambda tag: tag.name == "h3" and "作者介紹" in tag.text)
    if author_intro_heading and author_intro_heading.find_next_sibling("div"):
        author_intro = author_intro_heading.find_next_sibling("div").text.strip()
    # else:
    #     print("作者介紹 not found or has no following div.")

    return {
        # # '網址': url,
        '商品類別': category_name,
        '中文書名': title,
        '原文書名': None,
        '書號': None,
        '出版社名稱': publisher,
        '出版日期': publish_date,
        '作者中文名': author,
        '作者外文名': None,
        '譯者': translator,
        'ISBNISSN': isbn,
        '定價': price,
        '中國圖書分類號': None,
        # 'Series': series,
        # '開數': spec[3] if len(spec) > 3 else None,
        # '平/精裝': spec[0] if len(spec) > 0 else None,
        # '頁數': spec[1] if len(spec) > 1 else None,
        # '版次': spec[5] if len(spec) > 5 else None,

        '開數': next((item for item in spec if 'cm' in item), None),
        '平/精裝': next((item for item in spec if '裝' in item), None),
        '頁數': next((item for item in spec if '頁' in item), None),
        # '頁數': next((int(''.join(filter(str.isdigit, item))) for item in spec if '頁' in item and ''.join(filter(str.isdigit, item)) != ''), 0),
        '版次': next((item for item in spec if '版' in item), None),
        '級別': next((item for item in spec if '級' in item), None),
        '印刷': next((item for item in spec if '刷' in item), None),

        # 'Publish Place': publish_place
        '圖片': img_url,
        '作者簡介': author_intro,
        '內容簡介': content_intro,
        '目錄': None,
        '得獎與推薦紀錄': None,
        '重要事件': None
    }


def upload_file_to_s3(file_path, bucket, object_name=None):
    # 如果沒有指定 object_name，則使用檔案名稱
    if object_name is None:
        object_name = os.path.basename(file_path)

    # 將存入 bucket 的路徑設定為 books/images
    object_name = os.path.join('books', 'images', object_name)

    # 從環境變數中獲取 AWS 憑證
    AwsAccessKeyId = os.environ['AwsAccessKeyId']
    AwsSecretAccessKey = os.environ['AwsSecretAccessKey']

    # 建立 S3 client
    s3 = boto3.client('s3', aws_access_key_id=AwsAccessKeyId, aws_secret_access_key=AwsSecretAccessKey)

    # 上傳檔案並設定為公開
    try:
        # with open(file_path, "rb") as data:
        # s3.upload_fileobj(data, bucket, object_name, ExtraArgs={'ACL': 'public-read'})
        s3.upload_fileobj(file_path, bucket, object_name, ExtraArgs={'ACL': 'public-read'})
        # print(f"Successfully uploaded {file_path} to {bucket}/{object_name}")
        return f"https://{bucket}.s3.amazonaws.com/{object_name}"
    except ClientError as e:
        # logging.error(e)
        # print(f"Failed to upload {e}")
        file_url = 's3 fail'
        return str(e)

    # 建立檔案的公開 URL

    return file_url
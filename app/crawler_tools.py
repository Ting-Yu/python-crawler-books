import logging

import requests
from botocore.exceptions import ClientError
from bs4 import BeautifulSoup

import time
import psutil
import os
import random

from datetime import datetime
import pandas as pd

import humanfriendly
import boto3

# Get the current timestamp
# timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
# 考量到正式環境可能會有多個使用者同時使用，因此將 timestamp 設定為固定值
timestamp = os.environ.get('DownloadPath', "no_set_downloads_path")

class Logger:
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def log_to_csv(self, data, filename):
        df = pd.DataFrame([data])
        df.to_csv(os.path.join(self.timestamp, 'logs', filename), mode='a', index=False)

    def write_to_file(self, content, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
        else:
            print(f"File {filename} already exists. Skipping write.")

    def log_url(self, url, success, status_code=None, message=None):
        # 建立一個字典來儲存 URL、成功或失敗的狀態、HTTP 狀態碼和訊息
        data = {'url': url, 'success': success, 'status_code': status_code, 'message': message}
        # 將資訊寫入 'url_log.csv' 檔案
        self.log_to_csv(data, 'url_log.csv')

def create_directory(dir_name):
    """Create a directory if it does not exist."""
    os.makedirs(dir_name, exist_ok=True)

def get_page_content(url):
    logger = Logger(timestamp)  # Create an instance of Logger
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        # response = requests.get(url, headers=headers, timeout=5)
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Check if the page contains the error message
            if "瀏覽方式錯誤" in soup.text or "Please check your ip address" in soup.text:
                print(f"Access blocked when attempting to get content from {url}")
                logger.log_to_csv({'url': url, 'http_code': response.status_code, 'message': 'Access blocked'},
                                  f'url_failed-{logger.timestamp}.csv')
                logger.log_url(url, False, response.status_code, 'Access blocked')  # 記錄失敗的 URL 和 HTTP 狀態碼
                return None
            print(f"Successfully got content from {url}")
            time.sleep(random.randint(2, 5))  # pause for 2 to 5 seconds
            # Record success
            logger.log_to_csv({'url': url, 'http_code': response.status_code, 'message': 'Success'}, f'url_success-{logger.timestamp}.csv')
            logger.log_url(url, True, response.status_code, 'Success')  # 記錄成功的 URL 和 HTTP 狀態碼
            return soup
        else:
            print(f"Failed to get content from {url}")
            # Record failure
            logger.log_to_csv({'url': url, 'http_code': response.status_code, 'message': 'Failed'}, f'url_failed-{logger.timestamp}.csv')
            logger.log_url(url, False, response.status_code, 'Failed')  # 記錄失敗的 URL 和 HTTP 狀態碼
            return None
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        print(f"HTTP error for {url} occurred with status code {status_code}: {e}")

        logger.log_to_csv({'url': url, 'http_code': 'N/A', 'message': str(e)},
                          f'url_failed-{logger.timestamp}.csv')
        logger.log_url(url, False, status_code, 'Failed')  # 記錄失敗的 URL 和 HTTP 狀態碼
        return None
    except requests.exceptions.RequestException as e:
        status_code = e.response.status_code
        print(f"Request error for {url}: {e}")
        logger.log_to_csv({'url': url, 'http_code': 'N/A', 'message': str(e)},
                          f'url_failed-{logger.timestamp}.csv')
        logger.log_url(url, False, status_code, 'Failed')  # 記錄失敗的 URL 和 HTTP 狀態碼
        return None

def download_image(img_url, filename):
    logger = Logger(timestamp)  # Create an instance of Logger
    # 在檔案名稱中添加子目錄
    filename = os.path.join(logger.timestamp, 'images', filename)
    # 檢查目錄是否存在，如果不存在則創建
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    # 發送 GET 請求並將回應的內容保存為圖片
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            # Record success
            logger.log_to_csv({'url': img_url, 'http_code': response.status_code, 'message': 'Success'}, f'image_success-{logger.timestamp}.csv')
            logger.log_url(img_url, True, response.status_code, 'Success')  # 記錄成功的 URL 和 HTTP 狀態碼
            return filename
        else:
            # Record failure
            logger.log_to_csv({'url': img_url, 'http_code': response.status_code, 'message': 'Failed'}, f'image_failed-{logger.timestamp}.csv')
            logger.log_url(img_url, False, response.status_code, 'Failed')  # 記錄失敗的 URL 和 HTTP 狀態碼
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        print(f"HTTP error for {img_url} occurred with status code {status_code}: {e}")
        logger.log_to_csv({'url': img_url, 'http_code': 'N/A', 'message': str(e)},
                          f'image_failed-{logger.timestamp}.csv')
        logger.log_url(img_url, False, status_code, 'Failed')  # 記錄失敗的 URL 和 HTTP 狀態碼
    except requests.exceptions.RequestException as e:
        status_code = e.response.status_code
        print(f"Request error for {img_url}: {e}")
        logger.log_to_csv({'url': img_url, 'http_code': 'N/A', 'message': str(e)},
                          f'image_failed-{logger.timestamp}.csv')
        logger.log_url(img_url, False, status_code, 'Failed')  # 記錄失敗的 URL 和 HTTP 狀態碼
def write_soup_to_file(soup, filename):
    logger = Logger(timestamp)  # Create an instance of Logger
    filename = os.path.join(logger.timestamp, 'htmls', filename)
    logger.write_to_file(str(soup.prettify()), filename)

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

    spec_elem = soup.find('li', string=lambda x: x and '規格' in x)
    if spec_elem:
        spec = spec_elem.text.strip().split('：')[-1]
        # 使用 '/' 符號進行切割
        spec_parts = spec.split('/')
        spec = [part.strip() for part in spec_parts]
    else:
        spec = []

    publish_place_elem = soup.find('li', string=lambda x: x and '出版地' in x)
    publish_place = publish_place_elem.text.strip().split('：')[-1] if publish_place_elem else None

    img_elem = soup.find('img', {'class': 'cover M201106_0_getTakelook_P00a400020052_image_wrap'})
    img_url = img_elem['src'] if img_elem else None

    author_intro_elem = soup.find('div', {'class': 'content', 'style': 'height:auto;'})
    author_intro = author_intro_elem.text.strip() if author_intro_elem else None

    content_intro_elem = soup.find('div', {'class': 'content', 'style': 'height:auto;'})
    content_intro = content_intro_elem.text.strip() if content_intro_elem else None

    return {
        # '網址': url,
        '商品類別': category_name,
        '中文書名': title,
        '原文書名': None,
        '書號': None,
        '出版社名稱': publisher,
        '出版日期': publish_date,
        '作者中文名': author,
        '作者外文名': None,
        '譯者': translator,
        'ISBN/ISSN': isbn,
        '定價': price,
        '中國圖書分類號': None,
        # 'Series': series,
        '開數': next((item for item in spec if 'cm' in item), None),
        '平/精裝': next((item for item in spec if '裝' in item), None),
        '頁數': next((int(''.join(filter(str.isdigit, item))) for item in spec if
                      '頁' in item and ''.join(filter(str.isdigit, item)) != ''), 0),
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

def export_excel(book_data):
    # 產生 Excel 檔案名稱
    excel_filename = f"book_info_{timestamp}.xlsx"

    # 將檔案路徑改為新建立的資料夾
    filename = os.path.join(timestamp, excel_filename)
    # 將字典列表轉換為 DataFrame
    df = pd.DataFrame(book_data)

    # 將 DataFrame 輸出到 Excel 檔案
    df.to_excel(filename, index=False)

    print(f"The number of Books is {len(book_data)}")

def upload_file_to_s3(file_path, bucket, object_name=None):
    # 如果沒有指定 object_name，則使用檔案名稱
    if object_name is None:
        object_name = os.path.basename(file_path)

    # 將存入 bucket 的路徑設定為 books/images
    object_name = os.path.join('books', 'images', object_name)

    # 從環境變數中獲取 AWS 憑證
    AwsAccessKeyId = os.environ.get('AwsAccessKeyId')
    AwsSecretAccessKey = os.environ.get('AwsSecretAccessKey')

    # 建立 S3 client
    s3 = boto3.client('s3', aws_access_key_id=AwsAccessKeyId, aws_secret_access_key=AwsSecretAccessKey)

    # 上傳檔案並設定為公開
    try:
        with open(file_path, "rb") as data:
            s3.upload_fileobj(data, bucket, object_name, ExtraArgs={'ACL': 'public-read'})
        print(f"Successfully uploaded {file_path} to {bucket}/{object_name}")
    except ClientError as e:
        logging.error(e)
        print(f"Failed to upload {e}")
        return None

    # 建立檔案的公開 URL
    file_url = f"https://{bucket}.s3.amazonaws.com/{object_name}"

    return file_url

class PerformanceMonitor:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.start_time = None
        self.start_datetime = None
        self.start_memory = None
        self.end_time = None
        self.end_datetime = None
        self.end_memory = None

    def start(self):
        self.start_time = time.time()
        self.start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.start_memory = self.process.memory_info().rss

    def stop(self):
        self.end_time = time.time()
        self.end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_memory = self.process.memory_info().rss

    def report(self):
        execution_time = self.end_time - self.start_time
        memory_usage = self.end_memory - self.start_memory

        print(f"The program started at {self.start_datetime}.")
        print(f"The program ended at {self.end_datetime}.")

        execution_time = humanfriendly.format_timespan(execution_time)
        memory_usage = humanfriendly.format_size(memory_usage)

        print(f"The program took {execution_time} to complete.")
        print(f"The loop used {memory_usage} of memory.")
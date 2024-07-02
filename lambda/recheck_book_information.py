import json
from urllib.parse import urlparse
import tools


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
            result = crawl_book_info(url)

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


def crawl_book_info(url):
    # return tools.timestamp
    book_info = {}  # 建立一個空字典來儲存書的資訊

    path = urlparse(url).path
    # filename = os.path.basename(path)
    # Create the required directories
    # tools.create_directory(timestamp)
    # tools.create_directory(os.path.join(timestamp, 'logs'))
    # tools.create_directory(os.path.join(timestamp, 'htmls'))
    # tools.create_directory(os.path.join(timestamp, 'images'))

    soup = tools.get_page_content(url)  # Pass the logger instance as an argument
    # return soup
    if soup is not None:
        # filename = f"output_{filename}.html"
        # 將 soup 寫入檔案
        # tools.write_soup_to_file(soup, filename)  # Pass the logger instance as an argument

        # 解析資料
        book_info = extract_book_info(url, soup)

        # 下載圖片
        # img_url = book_info.get('圖片')
        # if img_url:
        #     img_filename = f"download_{filename.split('.')[0]}.jpg"
        #     tools.download_image(img_url, img_filename)  # Pass the logger instance as an argument

    return book_info


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
        '網址': url,
        'ISBN/ISSN': isbn,
        '中文書名': title,
        '出版社名稱': publisher,
        '出版日期': publish_date,
        '定價': price,
    }
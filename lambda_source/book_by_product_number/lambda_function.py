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
    # soup = get_page_content(url)  # Pass the logger instance as an argument
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

    parent_div = soup.find('div', class_='type02_p003 clearfix')
    author_elems = parent_div.find_all('a', href=lambda x: x and 'adv_author' in x) if parent_div else []

    # 解析作者、譯者、繪者
    author = None
    author_foreign = None
    translator = None
    draftsman = None

    for elem in author_elems:
        previous_text = elem.find_previous(text=True).strip() if elem.find_previous(text=True) else ''
        if '作者' in previous_text and author is None:
            author = elem.text.strip()
        elif '原文作者' in previous_text and author_foreign is None:
            author_foreign = elem.text.strip()
        elif '譯者' in previous_text and translator is None:
            translator = elem.text.strip()
        elif '繪者' in previous_text and draftsman is None:
            draftsman = elem.text.strip()

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
        spec_raw = spec_elem.text.strip().split('：')[-1]
        spec_parts = spec_raw.split('/')
        spec = [part.strip() for part in spec_parts if part.strip()]
    else:
        spec = []

    publish_place_elem = soup.find('li', string=lambda x: x and '出版地' in x)
    publish_place = publish_place_elem.text.strip().split('：')[-1] if publish_place_elem else None

    img_elem = soup.find('img', {'class': 'cover M201106_0_getTakelook_P00a400020052_image_wrap'})
    img_url = img_elem['src'] if img_elem else None

    # 內容簡介
    content_intro = None
    content_intro_heading = soup.find(lambda tag: tag.name == "h3" and "內容簡介" in tag.text)
    if content_intro_heading and content_intro_heading.find_next_sibling("div"):
        content_intro = content_intro_heading.find_next_sibling("div").text.strip()

    # 作者介紹
    author_intro = None
    author_intro_heading = soup.find(lambda tag: tag.name == "h3" and "作者介紹" in tag.text)
    if author_intro_heading and author_intro_heading.find_next_sibling("div"):
        author_intro = author_intro_heading.find_next_sibling("div").text.strip()

    # 目錄
    agenda = None
    agenda_heading = soup.find(lambda tag: tag.name == "h3" and "目錄" in tag.text)
    if agenda_heading and agenda_heading.find_next_sibling("div"):
        agenda = agenda_heading.find_next_sibling("div").text.strip()

    return {
        # # '網址': url,
        '商品類別': category_name,
        '中文書名': title,
        '原文書名': None,
        '書號': None,
        '出版社名稱': publisher,
        '出版日期': publish_date,
        '作者中文名': author,
        '作者外文名': author_foreign,
        '譯者': translator,
        '繪者': draftsman,
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
        '目錄': agenda,
        '得獎與推薦紀錄': None,
        '重要事件': None
    }
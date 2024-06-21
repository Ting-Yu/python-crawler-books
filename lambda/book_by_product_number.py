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
        book_info = tools.extract_book_info(url, soup)

        # 下載圖片
        # img_url = book_info.get('圖片')
        # if img_url:
        #     img_filename = f"download_{filename.split('.')[0]}.jpg"
        #     tools.download_image(img_url, img_filename)  # Pass the logger instance as an argument

    return book_info
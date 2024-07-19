import models.publisher as publisher_model
import models.book as book_model
import models.sqlalchemy_config as sqlalchemy_config
import pandas as pd

import os
import pandas as pd


def replace_nan_with_none(book_data):
    """
    Replace any nan values in the book_data dictionary with None.
    This function can be expanded to handle specific fields differently if needed.
    """
    for key, value in book_data.items():
        if pd.isna(value):
            book_data[key] = None
    return book_data


def save_upsert_data_to_csv(upsert_data_list, file_number):
    if upsert_data_list:
        # Ensure the saves directory exists
        save_path = 'saves'
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Convert the list of dictionaries to a DataFrame
        result_df = pd.DataFrame(upsert_data_list)
        # Specify the column order using the keys from the first dictionary in the list
        column_order = list(upsert_data_list[0].keys())
        # Construct the CSV file name with the saves directory
        csv_file_name = os.path.join(save_path, f'save_{file_number}.csv')
        # Save the DataFrame to a CSV file with the specified column order
        result_df.to_csv(csv_file_name, index=False, columns=column_order)
        print(f"Data saved to {csv_file_name}")


def handle_success(book_result):
    print(f"@@@ Success Book ...book id: {book_result.book_id} , Status: True @@@")


def handle_error(book_id, isbn, title, status, book_result):
    error_message = getattr(book_result, 'message', 'No error message available')
    # print(f"{book_result}")
    # input("Press Enter to continue...")
    print(f"************")
    print(f"*** Error Book ...book id : {book_id} , isbn : {isbn} , title : {title} , Status: {status}  ***")
    print(f" Error Message : {error_message}")
    print(f"************")
    # input("*** Error Book ...")


def recheck_book():
    db = sqlalchemy_config.get_db()

    publishers = publisher_model.get_all_publishers(db, [], skip=0, limit=10000)
    publisher_dict = {publisher.name: publisher for publisher in publishers}
    # print(f"*** Publisher Dict: {publisher_dict}")

    # Specify the path to your Excel file
    for file_number in range(0, 56):
        excel_file_path = 'compare_excel/書目資料_table' + str(file_number) + '.xlsx'
        print(f"*** Excel File Path: {excel_file_path}")

        # Read the Excel file
        # By default, this reads the first sheet. You can specify a sheet name with the `sheet_name` parameter.
        df = pd.read_excel(excel_file_path, engine='openpyxl')

        # missing_book_ids = []  # List to store book_ids not found in the database
        #
        # for index, row in df.iterrows():
        #     book_id = row['book_id']
        #     if book_id not in database_of_books_dict:
        #         missing_book_ids.append(book_id)

        # Now, missing_book_ids contains all the book_ids from the DataFrame that are not in database_of_books_dict
        # You can print them or process them as needed
        # Convert DataFrame book_id column to a set
        df_book_ids = set(df['book_id'])

        database_of_books = book_model.get_all_books(db, [
            book_model.Book.book_id.in_(df_book_ids),
        ], skip=0, limit=len(df_book_ids))
        database_of_books_dict = {book.book_id: book for book in database_of_books}
        # print(f"*** Total Books: {len(database_of_books)}")

        # Convert database book_ids to a set
        database_book_ids = set(database_of_books_dict.keys())

        # Find missing book_ids by performing a set difference
        missing_book_ids = df_book_ids - database_book_ids
        if (len(missing_book_ids) > 0):
            print("Missing Book IDs:", missing_book_ids)
            # input("Press Enter to continue...")

        if len(missing_book_ids) > 0:
            upsert_data_list = []
            filtered_df = df.loc[df['book_id'].isin(missing_book_ids)]
            # Display the first few rows of the dataframe
            # print(df.head())
            # print(f"*** Total Rows: {len(df)}")
            # for index, row in df.iterrows():
            for index, row in filtered_df.iterrows():
                # print(f"*** Row {index}")
                book_id = row['book_id']
                isbn = row['isbn']
                if pd.isnull(isbn) or isbn == '':
                    isbn = None
                title = row['書名']
                publisher_name = row['出版社']
                publisher_id = 9999
                if publisher_name in publisher_dict:
                    publisher_id = publisher_dict[publisher_name].publisher_id
                published_at = row['出版日']
                if pd.isnull(published_at):
                    published_at = None
                author = row['作者']
                if pd.isnull(author) or author == '':
                    author = ''
                translator = row['翻譯']
                price = row['定價']
                if pd.isnull(price):
                    price = 0
                tax = row['稅別']
                sale_discount = row['銷折']
                purchase_discount = row['進折']
                if publisher_id != 9999:
                    sale_discount = publisher_dict[publisher_name].sale_discount
                    purchase_discount = publisher_dict[publisher_name].purchase_discount
                cover = row['圖片路徑']
                # 確保 cover 是一個字符串
                if isinstance(cover, str):
                    cover = cover.replace('~/Img', 'https://fribooker.s3.amazonaws.com/books/prev')
                # else:
                #     cover = 'https://fribooker.s3.amazonaws.com/books/default_cover.jpg'
                description = row['內容簡介']
                author_intro = row['作者簡介']
                catalog = row['目錄']

                upsert_data = {
                    'book_id': book_id,
                    'book_crawler_id': 0,
                    'isbn': isbn,
                    'title': title,
                    'publisher_id': publisher_id,
                    'published_at': published_at,
                    'author': author,
                    'translator': translator,
                    'cover': cover,
                    'price': price,
                    'description': description,
                    'author_intro': author_intro,
                    'origin_title': '',
                    'author_foreign': '',
                    'open_number': '',
                    'soft_hard_cover': '',
                    'page_count': 0,
                    'edition': '',
                    'important_event': '',
                    'book_number': '',
                    'publisher_name': publisher_name,
                    'catalog': catalog,
                    'reward_history': '',
                    'china_book_class': '',
                    'tax': tax,
                    'sale_discount': sale_discount,
                    'purchase_discount': purchase_discount,
                    'stock': 0,
                    'status': 1,
                    'book_type': 1,
                    'can_refund': 0,
                    'limit_count': 0,
                }
                upsert_data = replace_nan_with_none(upsert_data)
                # print(upsert_data)
                upsert_data_list.append(upsert_data)

                [book_result, status] = book_model.upsert_book(db, upsert_data)
                if status:
                    handle_success(book_result)
                else:
                    handle_error(book_id, isbn, title, status, book_result)

            if len(upsert_data_list) > 0:
                # batch_insert_with_chunks(upsert_data_list, 100)
                save_upsert_data_to_csv(upsert_data_list, file_number)
            # input("Press Enter to continue...")

    db.close()


def chunked_list(input_list, chunk_size):
    """Yield successive chunk_size chunks from input_list."""
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i:i + chunk_size]


def batch_insert_with_chunks(upsert_data_list, chunk_size=50):
    """Insert data in chunks."""
    for chunk in chunked_list(upsert_data_list, chunk_size):
        try:
            print(f"Inserting chunk of {len(chunk)} records")
            print(f"Chunk All Book Ids: {', '.join(str(book['book_id']) for book in chunk)}")
            # input("chunk Press Enter to continue...")
            # Assuming bulk_insert_books is a function that handles the insertion logic
            book_model.bulk_insert_books(chunk)
            # input("bulk_insert_books Press Enter to continue...")
        except Exception as e:
            print(f"An error occurred during batch insert of a chunk: {e}")
            # Optionally, log the chunk or error for further analysis


if __name__ == '__main__':
    recheck_book()

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

    # Specify the path to your Excel file
    excel_file_path = 'modify_excel/20240724.xlsx'
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

    for index, row in df.iterrows():
        # print(f"{row}")
        # print(f"{index}")
        row_processed = replace_nan_with_none(row)

        book_id = row_processed['book_id']
        isbn = row_processed['isbn']
        title = row_processed['title']
        method = row_processed['處理方式']
        answer = row_processed['answer']

        if book_id:
            try:
                match method:
                    # case "刪除":
                    #     # print(f"刪除*** Book ID: {book_id}, ISBN: {isbn}, Title: {title}, Method: {method}, Answer: {answer}")
                    #     delete_book(db, book_id)
                    # case "絕版":
                    #     # print(f"絕版*** Book ID: {book_id}, ISBN: {isbn}, Title: {title}, Method: {method}, Answer: {answer}")
                    #     exhausted_book(db, book_id)
                    # case "保留":
                    #     print(f"保留*** Book ID: {book_id}, ISBN: {isbn}, Title: {title}, Method: {method}, Answer: {answer}")
                    case "修改ISBN":
                        if answer:
                            # print(
                                # f"修改ISBN*** Book ID: {book_id}, ISBN: {isbn}, Title: {title}, Method: {method}, Answer: {answer}")
                            fix_isbn_book(db, book_id, answer)
                        else:
                            print(
                                f"修改ISBN*** Book ID: {book_id}, ISBN: {isbn}, Title: {title}, Method: {method}, Answer: {answer}")
            except Exception as e:
                print('------------------------')
                print(f"*** Error: {e}")
                print(f"*** Row {row}")
                print('------------------------')
        else:
            print(f"*** Row {row}")

    input("Success Press Enter to continue...")


def delete_book(db: sqlalchemy_config.Session, book_id: int):
    book_model.delete_book_by_id(db, book_id)


def exhausted_book(db: sqlalchemy_config.Session, book_id: int):
    book_model.update_book_by_book_id(db, book_id, {'status': 4})


def replace_nan_with_none(book_data):
    for key, value in book_data.items():
        if pd.isna(value):
            book_data[key] = None
    return book_data

def fix_isbn_book(db: sqlalchemy_config.Session, book_id: int, isbn: str):
    # Ensure ISBN is not NaN and is a string
    if pd.isna(isbn):
        print(f"ISBN for book_id {book_id} is NaN. Skipping update.")
        return
    isbn = str(isbn)  # Explicitly convert to string to avoid any type issues
    book_model.update_book_by_book_id(db, book_id, {'isbn': isbn})



if __name__ == '__main__':
    recheck_book()

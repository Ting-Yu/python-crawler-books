import models.book as book_model
import models.shipping_item as shipping_model
import models.sqlalchemy_config as sqlalchemy_config


def recheck_shipping_item_book():
    db = sqlalchemy_config.get_db()
    page = 1
    page_size = 100

    while True:
        shipping_items = shipping_model.get_paginated_shippings(db, [
            shipping_model.ShippingItem.book_id.is_(None),
            shipping_model.ShippingItem.temp_isbn.is_not(None),
        ], page=page, page_size=page_size)
        print(f"Page: {page}, Shipping Items: {len(shipping_items.items)}")
        if not shipping_items:
            break
        print(f"Continuing to process {len(shipping_items.items)} shipping items...")
        shipping_item_book_isbns = [item.temp_isbn for item in shipping_items.items]
        # print(f"shipping_item_book_isbns:{shipping_item_book_isbns}")
        books = book_model.get_book_by_isbns(db, shipping_item_book_isbns)
        book_isbns = [book.isbn for book in books]
        # shipping_item_book_temp_book_names = [item.temp_book_name for item in shipping_items.items]
        # # print(f"shipping_item_book_isbns:{shipping_item_book_isbns}")
        # books = book_model.get_book_by_titles(db, shipping_item_book_temp_book_names)
        # book_titles = [book.title for book in books]

        isbn_count = {}
        for book in books:
            if book.isbn in isbn_count:
                isbn_count[book.isbn] += 1
            else:
                isbn_count[book.isbn] = 1
        unique_books = [book for book in books if isbn_count[book.isbn] == 1]

        books_dict = {book.isbn: book for book in unique_books}
        # books_dict = {book.title: book for book in unique_books}
        # print(f"book_isbns:{book_isbns}")

        filtered_shipping_item_book_isbns = [isbn for isbn in shipping_item_book_isbns if isbn in book_isbns]
        # filtered_shipping_item_book_names = [book_name for book_name in shipping_item_book_temp_book_names if book_name in book_titles]
        # print(f"Page: {page}, Shipping Items: {len(shipping_item_book_isbns)}, Books: {len(book_isbns)}, Filtered: {len(filtered_shipping_item_book_isbns)}")
        # print(f"filtered_shipping_item_book_isbns:{filtered_shipping_item_book_isbns}")

        updates = []
        if len(filtered_shipping_item_book_isbns) > 0:
            for item in shipping_items.items:
                shipping_id = item.id
                book_name = item.temp_book_name
                isbn = item.temp_isbn
                book = books_dict.get(isbn)
                if book:
                    book_id = book.book_id
                    # print(f"Book ID: {book_id} for ISBN: {isbn}")
                    updates.append({
                        "id": shipping_id,
                        "book_id": book_id,
                        "isbn": isbn
                    })

        if updates:
            print(f"Updating {len(updates)} books...")
            print(f"Chunk All Book Ids: {', '.join(str(book['id']) for book in updates)}")
            # print(f"Chunk All Book Sale Discount: {', '.join(str(book['sale_discount']) for book in updates)}")
            # print(f"Chunk All Book Purchase Discount: {', '.join(str(book['purchase_discount']) for book in updates)}")
            print("----------------")
            # input("Press Enter to continue...")
            print(f"{updates}")
            input("Press Enter to continue...")
            # shipping_model.update_shipping_item_in_chunks(db, updates)

        page += 1

        # input("Press Enter to continue...")

    db.close()


if __name__ == '__main__':
    recheck_shipping_item_book()

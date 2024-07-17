import models.book as book_model
import models.shipping_item as shipping_model
import models.sqlalchemy_config as sqlalchemy_config

def recheck_shipping_item_book():
    db = sqlalchemy_config.get_db()
    page = 1
    page_size = 50

    while True:
        shipping_items = shipping_model.get_paginated_shippings(db, [
            shipping_model.ShippingItem.book_id.is_(None),
            shipping_model.ShippingItem.temp_isbn.is_not(None),
        ], page=page, page_size=page_size)
        if not shipping_items:
            break
        # shipping_item_book_isbns = [item.isbn for item in shipping_items.items]
        #
        # books = book_model.get_book_by_isbns(db, shipping_item_book_isbns)
        # book_isbns = [book.isbn for book in books]
        #
        # filtered_shipping_item_book_isbns = [isbn for isbn in shipping_item_book_isbns if isbn in book_isbns]
        # print(f"Page: {page}, Shipping Items: {len(shipping_item_book_isbns)}, Books: {len(book_isbns)}, Filtered: {len(filtered_shipping_item_book_isbns)}")
        # common_isbns = [isbn for isbn in shipping_item_book_isbns if isbn in book_isbns]
        # print("ISBNs in both shipping items and books:", common_isbns)

        for item in shipping_items.items:
            isbn = item.temp_isbn
            # print(f"Shipping Item ID: {item.book_id}, ISBN: {item.temp_isbn}")
            url = "https://search.books.com.tw/search/query/key/"+isbn

        page += 1

    db.close()


if __name__ == '__main__':
    recheck_shipping_item_book()
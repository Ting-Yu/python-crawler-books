import models.publisher as publisher_model
import models.book as book_model
import models.sqlalchemy_config as sqlalchemy_config


def recheck_book():
    db = sqlalchemy_config.get_db()

    publishers = publisher_model.get_all_publishers(db, [], skip=0, limit=10000)
    # print(f"*** Total Publishers: {len(publishers)}")
    publisher_dict = {publisher.publisher_id: publisher for publisher in publishers}
    # print(f"*** Publisher Dict: {publisher_dict}")

    page = 1
    page_size = 1000
    while True:
        books = book_model.get_paginated_books(db, [
            book_model.Book.sale_discount == 0,
            book_model.Book.purchase_discount == 0,
        ], page=page, page_size=page_size).items
        if len(books) == 0:
            break

        for book in books:
            book_id = book.book_id
            publisher_id = book.publisher_id
            if publisher_id in publisher_dict:
                sale_discount = publisher_dict[publisher_id].sale_discount
                purchase_discount = publisher_dict[publisher_id].purchase_discount
                print(f"*** Book {book_id} Sale Discount: {sale_discount}, Purchase Discount: {purchase_discount}")

                book_model.update_book_by_book_id(db, book_id, {
                    "sale_discount": sale_discount,
                    "purchase_discount": purchase_discount,
                })
            else:
                print(f"*** Book -- {publisher_id} -- Publisher Not Found")

        page += 1

    db.close()


if __name__ == '__main__':
    recheck_book()

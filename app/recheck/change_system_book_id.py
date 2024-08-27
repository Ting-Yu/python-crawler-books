import models.publisher as publisher_model
import models.book as book_model
import models.sqlalchemy_config as sqlalchemy_config
import models.supplier as supplier_model
import requests
from itertools import cycle
import time
import os
import json
import re
import models.order_item as order_item_model
import models.purchase_item as purchase_item_model
import models.stock_history as stock_history_model
import models.stock_item as stock_item_model
import models.cart as cart_model
import models.next as next_model
import models.shipping_item as shipping_item_model


def search_shipping_item_by_temp_isbn(isbns):
    db = sqlalchemy_config.get_db()
    for isbn, book_info in isbns.items():
        temp_isbn = isbn
        book_info_new_book_id = book_info["new_book_id"]

        shipping_items = shipping_item_model.get_shipping_item_by_temp_isbn(db, temp_isbn)

        if shipping_items:
            for shipping_item in shipping_items:
                book_id = shipping_item.book_id
                if book_id is None:
                    print(
                        f"Null Shipping Item: {shipping_item.id} | {shipping_item.temp_isbn} | {shipping_item.book_id} | {book_info_new_book_id}")
                    shipping_item_model.update_shipping_item_by_temp_isbn(db, temp_isbn,
                                                                          {"book_id": book_info_new_book_id})

                else:
                    if book_id == book_info_new_book_id:
                        print(
                            f"Success Shipping Item: {shipping_item.id} | {shipping_item.temp_isbn} | {shipping_item.book_id} | {book_info_new_book_id}")
                    else:
                        print(
                            f"Error Shipping Item: {shipping_item.id} | {shipping_item.temp_isbn} | {shipping_item.book_id} | {book_info_new_book_id}")
                        shipping_item_model.update_shipping_item_by_temp_isbn(db, temp_isbn,
                                                                              {"book_id": book_info_new_book_id})

    db.close()

    # order_items.book_id
    # purchase_items.book_id
    # stock_history.book_id
    # stock_items.book_id
    # carts.book_id
    # nexts.book_id


def change_book_id(isbn, book_info):
    # order_items.book_id
    # purchase_items.book_id
    # stock_history.book_id
    # stock_items.book_id
    # carts.book_id
    # nexts.book_id

    book_info_isbn = isbn
    book_info_old_book_id = book_info["old_book_id"]
    book_info_new_book_id = book_info["new_book_id"]

    db = sqlalchemy_config.get_db()
    new_book = book_model.get_book_by_isbn(db, book_info_isbn)
    new_book_id = new_book.book_id

    old_book = book_model.get_book_by_id(db, book_info_old_book_id)
    old_book_id = old_book.book_id

    new_book = book_model.get_book_by_id(db, book_info_new_book_id)

    if new_book:
        print(
            f"Old Book ID: {old_book_id} = {book_info_old_book_id} | New Book ID: {new_book_id} = {book_info_new_book_id}")
        print(f"Old Book ISBN: {old_book.isbn} = {book_info_isbn} | New Book ISBN: {new_book.isbn} = {book_info_isbn} ")

        book_model.update_book_by_book_id(db, old_book_id, {"status": 99})

        carts = cart_model.get_cart_by_book_id(db, old_book_id)
        if carts:
            for cart in carts:
                print(f"Cart: {cart.cart_id} | {cart.book_id}")
            cart_model.update_cart_by_book_id(db, old_book_id, {"book_id": new_book_id})
            # input("Press Enter to continue...")

        nexts = next_model.get_next_by_book_id(db, old_book_id)
        if nexts:
            for next in nexts:
                print(f"Next: {next.next_id} | {next.book_id}")
            next_model.update_next_by_book_id(db, old_book_id, {"book_id": new_book_id})
        #         input("Press Enter to continue...")

        order_items = order_item_model.get_order_item_by_book_id(db, old_book_id)
        if order_items:
            for order_item in order_items:
                print(f"Order Item: {order_item.id} | {order_item.book_id}")
            order_item_model.update_order_item_by_book_id(db, old_book_id, {"book_id": new_book_id})
        #         input("Press Enter to continue...")

        purchase_items = purchase_item_model.get_purchase_item_by_book_id(db, old_book_id)
        if purchase_items:
            for purchase_item in purchase_items:
                print(f"Purchase Item: {purchase_item.id} | {purchase_item.book_id}")
            purchase_item_model.update_purchase_item_by_book_id(db, old_book_id, {"book_id": new_book_id})
        #         input("Press Enter to continue...")

        stock_histories = stock_history_model.get_stock_history_by_book_id(db, old_book_id)
        if stock_histories:
            for stock_history in stock_histories:
                print(f"Stock History: {stock_history.id} | {stock_history.book_id}")
            stock_history_model.update_stock_history_by_book_id(db, old_book_id, {"book_id": new_book_id})
        #         input("Press Enter to continue...")

        stock_items = stock_item_model.get_stock_item_by_book_id(db, old_book_id)
        if stock_items:
            for stock_item in stock_items:
                print(f"Stock Item: {stock_item.id} | {stock_item.book_id}")
            stock_item_model.update_stock_item_by_book_id(db, old_book_id, {"book_id": new_book_id})
        #         input("Press Enter to continue...")

        book_model.update_book_by_book_id(db, old_book_id, {"status": 99})
    else:
        print(f"Failed to get book by id: {old_book_id} | new book id {new_book_id} | isbn {book_info_isbn}")

    db.close()


if __name__ == '__main__':
    isbns = {
        9780020240785: {"new_book_id": 311118},
        9786267344330: {"new_book_id": 311491},
        9786263554955: {"new_book_id": 303340},
        9786269807659: {"new_book_id": 311457},
        731559258818: {"new_book_id": 293254},
        9789757901259: {"new_book_id": 308410},
        9789571365688: {"new_book_id": 311186},
        9786263582330: {"new_book_id": 311478},
        9789869986878: {"new_book_id": 311458},
        4713482020881: {"new_book_id": 301622},
        9786267244548: {"new_book_id": 311559},
        9786267250938: {"new_book_id": 311528},
        9786263775343: {"new_book_id": 301781},
        9786267401347: {"new_book_id": 310933},
        9789570829648: {"new_book_id": 311241}
    }
    search_shipping_item_by_temp_isbn(isbns)

    isbns = {
        9789866702211: {"old_book_id": 311086, "new_book_id": 17300},
        9789575998868: {"old_book_id": 311111, "new_book_id": 96175},
        9789861775906: {"old_book_id": 311126, "new_book_id": 34441},
        9789571339542: {"old_book_id": 311134, "new_book_id": 6223},
        9789579361811: {"old_book_id": 310893, "new_book_id": 19220},
        9789861776231: {"old_book_id": 311151, "new_book_id": 36383},
        9789575998950: {"old_book_id": 311152, "new_book_id": 96169},
        9789865925406: {"old_book_id": 311065, "new_book_id": 33633},
        9789867375469: {"old_book_id": 311239, "new_book_id": 16887},
        9789579501859: {"old_book_id": 311169, "new_book_id": 248256},
        9789570848137: {"old_book_id": 311188, "new_book_id": 126932},
        9789862133736: {"old_book_id": 310799, "new_book_id": 9103},
        9789868597983: {"old_book_id": 311226, "new_book_id": 13589},
        9789866631719: {"old_book_id": 311042, "new_book_id": 15345},
        9789861792835: {"old_book_id": 311171, "new_book_id": 35495},
        9789570823981: {"old_book_id": 311159, "new_book_id": 3976},
        9789867574268: {"old_book_id": 311158, "new_book_id": 39697},
        9789575705480: {"old_book_id": 311150, "new_book_id": 43305},
        9789865925017: {"old_book_id": 310930, "new_book_id": 33571},
        9789570842463: {"old_book_id": 310751, "new_book_id": 14437},
        9789866525285: {"old_book_id": 311072, "new_book_id": 19292},
        9789867108821: {"old_book_id": 311104, "new_book_id": 2051},
        9789866377297: {"old_book_id": 310873, "new_book_id": 12678},
        9789867059949: {"old_book_id": 165235, "new_book_id": 4770},
        9789866789212: {"old_book_id": 311055, "new_book_id": 16743},
        9789869114837: {"old_book_id": 311024, "new_book_id": 50703},
        9789866525384: {"old_book_id": 310132, "new_book_id": 19178},
        9789862728567: {"old_book_id": 311222, "new_book_id": 93687},
        9789866407659: {"old_book_id": 310969, "new_book_id": 34018},
        9789572958971: {"old_book_id": 311212, "new_book_id": 33755},
        9789577510730: {"old_book_id": 310898, "new_book_id": 89153},
        9789861774015: {"old_book_id": 311221, "new_book_id": 35593},
        9789869711340: {"old_book_id": 311027, "new_book_id": 248241},
        9789577517173: {"old_book_id": 310785, "new_book_id": 87636},
        9789577516152: {"old_book_id": 311066, "new_book_id": 88351},
        9789578491687: {"old_book_id": 128314, "new_book_id": 63466},
        9789867375261: {"old_book_id": 311224, "new_book_id": 16924},
        9789868867291: {"old_book_id": 310498, "new_book_id": 36857},
        9789570805215: {"old_book_id": 311045, "new_book_id": 8066},
        9789570827637: {"old_book_id": 310797, "new_book_id": 4162},
        9789573329862: {"old_book_id": 310849, "new_book_id": 139917},
        9789578221567: {"old_book_id": 146205, "new_book_id": 94738},
        9789574441402: {"old_book_id": 310908, "new_book_id": 13333},
        9789573049524: {"old_book_id": 310909, "new_book_id": 38883},
        9789578221444: {"old_book_id": 310131, "new_book_id": 94733},
        9789579525947: {"old_book_id": 310847, "new_book_id": 103252},
        9789869068574: {"old_book_id": 311235, "new_book_id": 106822},
        9789577621054: {"old_book_id": 310779, "new_book_id": 16713},
        9789573329350: {"old_book_id": 311249, "new_book_id": 139886},
        9789867375452: {"old_book_id": 310897, "new_book_id": 16818},
        9789868860339: {"old_book_id": 311227, "new_book_id": 106864},
        9789866789977: {"old_book_id": 311261, "new_book_id": 16687}
    }
    for isbn, book_info in isbns.items():
        change_book_id(isbn, book_info)

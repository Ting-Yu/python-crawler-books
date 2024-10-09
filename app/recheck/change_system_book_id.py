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

def search_shipping_item_by_temp_book_name(book_names):
    db = sqlalchemy_config.get_db()
    for book_name, book_info in book_names.items():
        temp_book_name = book_name
        book_info_new_book_id = book_info["new_book_id"]

        shipping_items = shipping_item_model.get_shipping_item_by_temp_book_name(db, temp_book_name)

        if shipping_items:
            for shipping_item in shipping_items:
                book_id = shipping_item.book_id
                if book_id is None:
                    print(
                        f"Null Shipping Item: {shipping_item.id} | {shipping_item.temp_book_name} | {shipping_item.book_id} | {book_info_new_book_id}")
                    shipping_item_model.update_shipping_item_by_temp_book_name(db, temp_book_name,
                                                                          {"book_id": book_info_new_book_id})

                else:
                    if book_id == book_info_new_book_id:
                        print(
                            f"Success Shipping Item: {shipping_item.id} | {shipping_item.temp_book_name} | {shipping_item.book_id} | {book_info_new_book_id}")
                    else:
                        print(
                            f"Error Shipping Item: {shipping_item.id} | {shipping_item.temp_book_name} | {shipping_item.book_id} | {book_info_new_book_id}")
                        shipping_item_model.update_shipping_item_by_temp_book_name(db, temp_book_name,
                                                                              {"book_id": book_info_new_book_id})

    db.close()

def change_book_id(isbn, book_info):

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
        9789571472591: {"new_book_id": 312572},
        4713510944288: {"new_book_id": 303242},
        977252053300918: {"new_book_id": 310118},
        9786267074794: {"new_book_id": 312574},
        9786267074800: {"new_book_id": 312576},
        9789888868124: {"new_book_id": 312606},
        9789887416241: {"new_book_id": 312577},
        9786263961357: {"new_book_id": 312578},
        9786267336915: {"new_book_id": 312579},
        9786263146167: {"new_book_id": 312580},
        9786267074930: {"new_book_id": 312581},
        9789865082963: {"new_book_id": 312582},
        9786267448502: {"new_book_id": 312583},
        9789864595990: {"new_book_id": 312584},
        9786263557161: {"new_book_id": 312585},
        9786263556713: {"new_book_id": 312586},
        9786263556690: {"new_book_id": 312587},
        9786263963030: {"new_book_id": 312588},
    }
    search_shipping_item_by_temp_isbn(isbns)

    book_names = {
        "形上學要義(二版)":{"new_book_id":312572},
        "鄉間小路 2月號/2024 第50卷第2期 餃好聚寶（過刊號買斷不退）__[收清日期:2024-04-10]":{"new_book_id":312589},
        "十月的天空(#2024全新修訂版)":{"new_book_id":303242},
        "鄉間小路 3月號/2024 第50卷第3期 樂鬧春遊（過刊號買斷不退）__[收清日期:2024-04-10]":{"new_book_id":312590},
        "《秋刀魚》冬季號/2023 第42期 現在就想吃的臺味日食":{"new_book_id":312595},
        "閱讀的島：友善書業合作社書店誌18【療癒與閱讀】":{"new_book_id":310118},
        "鄉間小路 4月號/2024 第50卷第4期 臺食新味__[收清日期:2024-07-25]":{"new_book_id":312591},
        "＜經典奇幻文學作家J. R. R. 托爾金1＞霍比特人":{"new_book_id":312574},
        "＜經典奇幻文學作家J. R. R. 托爾金2＞托爾金短篇故事集":{"new_book_id":312576},
        "英氣‧阿咩正傳(上)：一本你不知道的另類香港史":{"new_book_id":312606},
        "鄉間小路 5月號/2024 第50卷第5期 蜂和日蜜__[收清日期:2024-07-25]":{"new_book_id":312592},
        "共和國的饑餓：回顧我們的當下":{"new_book_id":312577},
        "《秋刀魚》春季號/2024 第43期 Taiwan -Japan 20代的我們":{"new_book_id":312597},
        "勇者系列／第五集：魔王與絕望勇者":{"new_book_id":312578},
        "鎌倉裏風景：在地人才知道的私藏路線X絕景秘境X深度文化，來場大人旅的深度休日提案":{"new_book_id":312579},
        "創業之國以色列【暢銷經典版】：教育思維＋兵役制度＋移民政策＋創投計畫，把逆境變成資產，樹立全球新創國家典範":{"new_book_id":312580},
        "花園裡的小宇宙：生物學家帶我們觀察與實驗，探索植物的祕密生活":{"new_book_id":312581},
        "一小時讀通世界金融史：從古羅馬帝國、羅斯柴爾德家族到金融海嘯，看懂國家興衰與金融巨頭崛起的意外真相！":{"new_book_id":312582},
        "盆栽急診室：葉子變黃、掉葉、病蟲害、換盆、修剪分枝，百年園藝老店繼承人的綠手指養護祕笈。":{"new_book_id":312583},
        "漫畫葡萄酒2：零基礎品酒養成記！從釀造原點拆解品飲技術，史上最強的餐酒搭配祕笈":{"new_book_id":312584},
        "小小科學人：100未知大發現":{"new_book_id":312585},
        "偵探狗超級任務1：誰是超級英雄？":{"new_book_id":312586},
        "偵探狗超級任務2：找出蛋糕小偷":{"new_book_id":312587},
        "別在該動腦子的時候動感情：看清親密關係的底層邏輯":{"new_book_id":312588},
    }
    search_shipping_item_by_temp_book_name(book_names)

    # isbns = {
    #     9789570535648: {"old_book_id": 309308, "new_book_id": 312249},
    #     9786267341391: {"old_book_id": 310929, "new_book_id": 311622},
    # }
    # for isbn, book_info in isbns.items():
    #     change_book_id(isbn, book_info)

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
        9789862899724: {"new_book_id": 301584},
        9786267373293: {"new_book_id": 311112},
        4711228588855: {"new_book_id": 301777},
        9786267382462: {"new_book_id": 310834},
        9786263775152: {"new_book_id": 301780},
        9789869702072: {"new_book_id": 311768},
        9786267338575: {"new_book_id": 302731},
        9786267356449: {"new_book_id": 301948},
        9786263746572: {"new_book_id": 302118},
        9786267378489: {"new_book_id": 302555},
        9786263145467: {"new_book_id": 302017},
        9789861786889: {"new_book_id": 302192},
        9786267421055: {"new_book_id": 303029},
        9786267401156: {"new_book_id": 302288},
        9786267388235: {"new_book_id": 302977},
        9786267314364: {"new_book_id": 301472},
        9786267388273: {"new_book_id": 303251},
        9789862943809: {"new_book_id": 310062},
        9786269814305: {"new_book_id": 310331},
        9789863876939: {"new_book_id": 302706},
        9786269792504: {"new_book_id": 302281},
        9786263748774: {"new_book_id": 304050},
        9786263748675: {"new_book_id": 303445},
        9786263900202: {"new_book_id": 303666},
        9786263207509: {"new_book_id": 304172},
        9786267388372: {"new_book_id": 304442},
        9786269827145: {"new_book_id": 311787},
        9786267388457: {"new_book_id": 304238},
        9786269693443: {"new_book_id": 304939},
        9786267338797: {"new_book_id": 304486},
        4710405009961: {"new_book_id": 312118},
        9786269782420: {"new_book_id": 304023},
        9786267421086: {"new_book_id": 304737},
        9786263614574: {"new_book_id": 304945},
        9786263154124: {"new_book_id": 310984},
        9786269821808: {"new_book_id": 310996},
        9786267234846: {"new_book_id": 305281},
        9786263749085: {"new_book_id": 304824},
        9786267255322: {"new_book_id": 305284},
        9786263582767: {"new_book_id": 304464},
        9789869024235: {"new_book_id": 305719},
        9786260120986: {"new_book_id": 312081},
        9786267430026: {"new_book_id": 304538},
        9786263748149: {"new_book_id": 303460},
        9786269786220: {"new_book_id": 304529},
        9789865082888: {"new_book_id": 305959},
        9786269778966: {"new_book_id": 305967},
        9786269814602: {"new_book_id": 306501},
        9786269814619: {"new_book_id": 306508},
        9786263749160: {"new_book_id": 305860},
        9786267293423: {"new_book_id": 306238},
        9786267283615: {"new_book_id": 305909},
        9786267382660: {"new_book_id": 303753},
        9786263749603: {"new_book_id": 305872},
        9786267262665: {"new_book_id": 305542},
        9786267356494: {"new_book_id": 303429},
        9786269821853: {"new_book_id": 303803},
        9786267368541: {"new_book_id": 310064},
        9786267263419: {"new_book_id": 303781},
        9786263748583: {"new_book_id": 306365},
        9789570873030: {"new_book_id": 306628},
        9786263556331: {"new_book_id": 303611},
        9786267388679: {"new_book_id": 307030},
        9789577418173: {"new_book_id": 306213},
        9786267338728: {"new_book_id": 305352},
        9786263748859: {"new_book_id": 304715},
        9786263960169: {"new_book_id": 307087},
        9786267339763: {"new_book_id": 307027},
        9786267243619: {"new_book_id": 306956},
        9786269821891: {"new_book_id": 305501},
        9786263106383: {"new_book_id": 306861},
        9786263106352: {"new_book_id": 306875},
        9786269517664: {"new_book_id": 311324},
        9786267454015: {"new_book_id": 310415},
        9786269819508: {"new_book_id": 304574},
        9786267284490: {"new_book_id": 307209},
        9786267074718: {"new_book_id": 303371},
        9789888822553: {"new_book_id": 302510},
        9786267366578: {"new_book_id": 304820},
        9786267283738: {"new_book_id": 307390},
        9786267401316: {"new_book_id": 310775},
        9789865082895: {"new_book_id": 307738},
        9789888809738: {"new_book_id": 308592},
        9786267298558: {"new_book_id": 306764},
        9786267367223: {"new_book_id": 304775},
        9789887416272: {"new_book_id": 312162},
        9789887416258: {"new_book_id": 312121},
        9789887416203: {"new_book_id": 312102},
        9786267074848: {"new_book_id": 307992},
        9786269821334: {"new_book_id": 307993},
        9786263961555: {"new_book_id": 310077},
        9786263960985: {"new_book_id": 308058},
        9786267063675: {"new_book_id": 308864},
        9786263616578: {"new_book_id": 308586},
        9786263145801: {"new_book_id": 308212},
        9786263960923: {"new_book_id": 308435},
        9786269848218: {"new_book_id": 310952},
        9786267209738: {"new_book_id": 304532},
        9786267408346: {"new_book_id": 308825},
        9786267338940: {"new_book_id": 307350},
        9786267378878: {"new_book_id": 309002},
        9786267378892: {"new_book_id": 309006},
        9786267388860: {"new_book_id": 312090},
        9786267338452: {"new_book_id": 307016},
        9786263960855: {"new_book_id": 308432},
        9786263960374: {"new_book_id": 307081},
        9786263208094: {"new_book_id": 308004},
        9786263615113: {"new_book_id": 306730},
        9789570873016: {"new_book_id": 307277},
        9786267293553: {"new_book_id": 309844},
        9786263900875: {"new_book_id": 309259},
        9786267375839: {"new_book_id": 309682},
        9786263980068: {"new_book_id": 309492},
        9786263980129: {"new_book_id": 309491},
        9789864064083: {"new_book_id": 309486},
        9789861798653: {"new_book_id": 309290},
        9789860682434: {"new_book_id": 309406},
        9786263106710: {"new_book_id": 309255},
        9789887416289: {"new_book_id": 310123},
        9786267356746: {"new_book_id": 309495},
        9786267275351: {"new_book_id": 310888},
        9786263146624: {"new_book_id": 310345},
        9786263208049: {"new_book_id": 309286},
        9771819917070: {"new_book_id": 312079},
        9771819917087: {"new_book_id": 312104},
        9786269820238: {"new_book_id": 308151},
        9786267234877: {"new_book_id": 307693},
        9786267460139: {"new_book_id": 307683},
        9786267262672: {"new_book_id": 308267},
        9786269782482: {"new_book_id": 307865},
        9786267336731: {"new_book_id": 311786},
        9786267421154: {"new_book_id": 305777},
        9786269852703: {"new_book_id": 309065},
        9789862626863: {"new_book_id": 311167},
        9786267401163: {"new_book_id": 308899},
        9870528081505: {"new_book_id": 310856},
        9870528081543: {"new_book_id": 312080},
        9786267445228: {"new_book_id": 311230},
        9786263749818: {"new_book_id": 307853},
        9786263749863: {"new_book_id": 308061},
        9789864899289: {"new_book_id": 307361},
        9789864899272: {"new_book_id": 307990},
        9786267483077: {"new_book_id": 310486},
        9786263146310: {"new_book_id": 311851},
        9789862590942: {"new_book_id": 310826},
        9786263106659: {"new_book_id": 310794},
        9786267440162: {"new_book_id": 310892},
        9786267405659: {"new_book_id": 311798},
        9786263901551: {"new_book_id": 310838},
        9786269839421: {"new_book_id": 310108},
        9786267394823: {"new_book_id": 310049},
        9786267234914: {"new_book_id": 310890},
        9786263208087: {"new_book_id": 311709},
        9786269839407: {"new_book_id": 310082},
        9786267376430: {"new_book_id": 310335},
        9789862626955: {"new_book_id": 311070},
        9789864064137: {"new_book_id": 311081},
        9786267255391: {"new_book_id": 310391},
        4711488870370: {"new_book_id": 309708},
        9786263057869: {"new_book_id": 308847},
        9786267428290: {"new_book_id": 305174},
        9786267188682: {"new_book_id": 305410},
        9786267376331: {"new_book_id": 311168},
        9786263961715: {"new_book_id": 311103},
    }
    search_shipping_item_by_temp_isbn(isbns)

    book_names = {
        "【春節暢銷書展】KUMA黑熊學院少年防衛課（專案期間：2024/2/1至2024/3/31，書店進價65折，需於2024/4/3前退回，逾期視同買斷）__【收清日期:2024-04-03】": {
            "new_book_id": 301038},
        "【春節暢銷書展】孤獨的哲學（專案期間：2024/2/1至2024/3/31，書店進價65折，需於2024/4/3前退回，逾期視同買斷）（售缺無庫存，暫無再刷再版計畫-20240227消息）__【收清日期:2024-04-03】": {
            "new_book_id": 300917},
        "我真的不知道自己怎麼會變擲筊怪的（限量簽名書）（買斷不退）": {"new_book_id": 310759},
        "【春節暢銷書展】走進布農的山（專案期間：2024/2/1至2024/3/31，書店進價65折，需於2024/4/3前退回，逾期視同買斷）__【收清日期:2024-04-03】": {
            "new_book_id": 278782},
        "【春節暢銷書展】島嶼拾光．文物藏影：臺灣文學的轉譯故事（專案期間：2024/2/1至2024/3/31，書店進價65折，需於2024/4/3前退回，逾期視同買斷）__【收清日期:2024-04-03】": {
            "new_book_id": 303285},
        "【春節暢銷書展】神明離去之後： 臺灣神社的收藏物語（專案期間：2024/2/1至2024/3/31，書店進價65折，需於2024/4/3前退回，逾期視同買斷）__【收清日期:2024-04-03】": {
            "new_book_id": 303264},
        "貢丸湯Vol.32 今仔日食菜": {"new_book_id": 311767},
        "《新活水》1月號/2024 第39期 ㄧ年之記": {"new_book_id": 311614},
        "《食力foodNEXT》No.34 一碗幹掉牛肉麵、陽春麵的 日式拉麵": {"new_book_id": 310667},
        "【友善專案】沙丘六部曲（無書盒套書．電影第二部書衣珍藏版）［專案期間2024/03/20~2024/05/03，63折出貨］(需於2024/05/04前退回，逾期視同買斷)__【收清日期:2024-05-04】": {
            "new_book_id": 303266},
        "【友善專案】托爾金傳說故事集：哈比人&魔戒【全新繁體中文譯本】（特價盒裝套書）［專案期間2024/03/20~2024/05/03，63折出貨］(需於2024/05/04前退回，逾期視同買斷)__【收清日期:2024-05-04】": {
            "new_book_id": 305927},
        "【春節暢銷書展】【平路台灣三部曲．三】夢魂之地（專案期間：2024/2/1至2024/3/31，書店進價65折，需於2024/4/3前退回，逾期視同買斷）__【收清日期:2024-04-03】": {
            "new_book_id": 303281},
        "〔公關書〕台灣山岳雜誌 No.161": {"new_book_id": 311487},
        "聯合文學 4月號/2024 第474期 作家的焦慮同好會": {"new_book_id": 311610},
        "薰風第26期-百藝齊綻 你所不知道的臺中文化城": {"new_book_id": 311613},
    }
    search_shipping_item_by_temp_book_name(book_names)

    # isbns = {
    #     9789570535648: {"old_book_id": 309308, "new_book_id": 312249},
    #     9786267341391: {"old_book_id": 310929, "new_book_id": 311622},
    # }
    # for isbn, book_info in isbns.items():
    #     change_book_id(isbn, book_info)

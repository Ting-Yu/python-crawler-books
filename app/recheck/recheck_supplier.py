import models.publisher as publisher_model
import models.book as book_model
import models.sqlalchemy_config as sqlalchemy_config
import models.supplier as supplier_model
import requests
from itertools import cycle
import time
import os
import json



def recheck_supplier():
    db = sqlalchemy_config.get_db()

    supplier = supplier_model.get_all_suppliers(db, [], skip=0, limit=10000)
    # print(f"*** Total Suppliers: {len(supplier)}")
    supplier_dict = {supplier.supplier_id: supplier for supplier in supplier}
    # print(f"*** Supplier Dict: {supplier_dict}")
    # input("Press Enter to continue...")

    page = 1
    page_size = 10000
    while True:
        suppliers = supplier_model.get_all_suppliers(db, [], skip=(page - 1) * page_size, limit=page_size)
        print(f"*** Page: {page} | Page Size: {page_size} | Total Books: {len(suppliers)}")
        # input("Press Enter to continue...")
        if len(suppliers) == 0:
            break

        updates = []
        for supplier in suppliers:
            supplier_id = supplier.supplier_id
            orn_return_goods = supplier.return_goods
            return_goods = supplier.return_goods

            if return_goods == None:
                return_goods = 1
            elif return_goods == "2":
                return_goods = 0
            else:
                return_goods = 1

            updates.append({
                "supplier_id": supplier_id,
                "return_goods": return_goods,
            })
            print(f"Book ID: {supplier_id} | Ori Return Goods :{orn_return_goods} | Return Goods: {return_goods}")

        if updates:
            print(f"Updating {len(updates)} books...")
            print("----------------")
            supplier_model.update_suppliers_in_chunks(db, updates)

        page += 1

    db.close()


if __name__ == '__main__':
    recheck_supplier()

import models.sqlalchemy_config as sqlalchemy_config
import models.book as book_model
import models.sales_return as sales_return_model
import models.sales_return_item as sales_return_item_model
import models.member as member_model


def check_sales_return_shipping(db):
    sales_returns = sales_return_model.get_all_sales_returns(db, [
        sales_return_model.SalesReturn.member_id.is_(None),
    ])

    for sales_return in sales_returns:
        sales_return_id = sales_return.sales_return_id
        member_temp_member_name = sales_return.temp_member_name
        member = member_model.get_member_by_name(db, member_temp_member_name)
        if member:
            member_id = member.id
            print(f"Sales Return ID: {sales_return_id} | Member: {member_id} = {member.name}")
            sales_return_model.update_sales_return_by_id(db, sales_return_id, {"member_id": member_id})
            db.commit()
            db.refresh(sales_return)
        else:
            print(f"***Error*** Sales Return ID: {sales_return_id} | Member: {member_temp_member_name} not found")


def check_sale_return_items(db):
    sales_return_items = sales_return_item_model.get_all_sales_return_items(db, [
        sales_return_item_model.SalesReturnItem.book_id.is_(None)
    ])

    for sales_return_item in sales_return_items:
        sales_return_item_id = sales_return_item.id
        temp_isbn = sales_return_item.temp_isbn

        book = book_model.get_book_by_isbn(db, temp_isbn)
        if book:
            book_id = book.book_id
            print(f"Sales Return Item ID: {sales_return_item_id} | Book ID: {book_id} = {book.title}")
            sales_return_item_model.update_sales_return_item_by_id(db, sales_return_item_id, {"book_id": book_id})
            db.commit()
            db.refresh(sales_return_item)
        else:
            print(
                f"***Error*** Sales Return Item ID: {sales_return_item_id} | Book Temp ISBN: {str(temp_isbn)} not found")


if __name__ == '__main__':
    db = sqlalchemy_config.get_db()

    check_sales_return_shipping(db)

    check_sale_return_items(db)

    db.close()

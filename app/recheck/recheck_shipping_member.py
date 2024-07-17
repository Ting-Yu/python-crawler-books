import models.member as member_model
import models.shipping as shipping_model
import models.sqlalchemy_config as sqlalchemy_config

def recheck_shipping_member():
    db = sqlalchemy_config.get_db()
    shippings = shipping_model.get_paginated_shippings(db, [
        shipping_model.Shipping.member_id.is_(None),
    ], page=1, page_size=1000).items

    members = member_model.get_members_all(db)
    member_dict = {member.name: member for member in members}
    # for member in members:
    #     print(f"Member: {member.id} = {member.name}")

    for shipping in shippings:
        shipping_id  = shipping.shipping_id
        member_id = shipping.member_id
        temp_member_name = shipping.temp_member_name

        for member_name in member_dict.keys():
            # print(f"*** Shipping {temp_member_name} Member: {member_id} = {member_name}")
            if member_name == temp_member_name:
                member = member_dict[member_name]
                print(f"*** Shipping {shipping_id} Member: {temp_member_name} = {member.name} = {member.id}")
                shipping_model.update_shipping_by_id(db, shipping_id, {"member_id": member.id})
                break

        # member = member_model.get_member_by_name(db, temp_member_name)
        # if member:
        #     print(f"*** Shipping {shipping_id} Member: {temp_member_name} = {member.name} = {member.id}")
        #     shipping.temp_member_name = member.name
        #     # db.commit()
        #     # db.refresh(shipping)
        # else:
        #     print(f"*** Shipping {shipping_id} Member: {member_id} = None ({temp_member_name})")

    db.close()


if __name__ == '__main__':
    recheck_shipping_member()
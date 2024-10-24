from be.model import error
from be.model import db_conn
import uuid
import json
import logging
from pymongo.errors import PyMongoError
from pymongo import MongoClient, errors  
from datetime import datetime

class Buyer(db_conn.DBConn):
    def __init__(self, user_db_name, store_db_name, book_db_name, order_db_name, store_book_db_name,history_orders_db_name):
        super().__init__(user_db_name, store_db_name, book_db_name, order_db_name, store_book_db_name,history_orders_db_name)

    def new_order():
        return
    
    # 确认收货后，更新订单状态为“已收货”
    def receive_books(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            # 1. 检查用户是否存在
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)

            # 2. 检查订单是否存在
            order = self.orders_collection.find_one({'_id': order_id})
            if not order:
                return error.error_invalid_order_id(order_id)

            # 3. 从订单中获取信息
            buyer_id = order['buyer_id']
            book_list = order['book_list']  # 获取书籍列表
            status = order['status']  # 订单状态

            # 4. 验证订单的买家身份
            if buyer_id != user_id:
                return error.error_authorization_fail()

            # 5. 验证订单的状态是否为“已发货” (status == "shipped")
            if status != "shipped":
                return error.error_invalid_order_status(order_id)

            # 6. 遍历订单的书籍列表，计算每个卖家的收入并更新卖家余额
            for book in book_list:
                store_book_id = book['store_book_id']
                quantity = book['quantity']
                price = book['price']
                total_price = quantity * price

                # 在 store_book_collection 中找到对应的 store_book_id 和卖家信息
                store_book = self.store_book_collection.find_one({'_id': store_book_id})
                if not store_book:
                    return error.error_invalid_store_book_id(store_book_id)

                seller_id = store_book['user_id']  # 获取卖家ID

                # 验证卖家是否存在
                if not self.user_id_exist(seller_id):
                    return error.error_non_exist_user_id(seller_id)

                # 更新卖家账户余额
                result = self.users_collection.update_one(
                    {"_id": seller_id},
                    {"$inc": {"balance": total_price}}  # 卖家增加订单书籍的收入
                )
                if result.matched_count == 0:
                    return error.error_non_exist_user_id(seller_id)

            # 7. 更新订单状态为“已收货”并记录收货时间
            self.orders_collection.update_one(
                {"_id": order_id},
                {
                    "$set": {
                        "status": "received",
                        "received_at": datetime.now()  # 设置收货时间
                    }
                }
            )

        except PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

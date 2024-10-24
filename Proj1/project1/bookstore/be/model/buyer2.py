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
    
    # ȷ���ջ��󣬸��¶���״̬Ϊ�����ջ���
    def receive_books(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            # 1. ����û��Ƿ����
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)

            # 2. ��鶩���Ƿ����
            order = self.orders_collection.find_one({'_id': order_id})
            if not order:
                return error.error_invalid_order_id(order_id)

            # 3. �Ӷ����л�ȡ��Ϣ
            buyer_id = order['buyer_id']
            book_list = order['book_list']  # ��ȡ�鼮�б�
            status = order['status']  # ����״̬

            # 4. ��֤������������
            if buyer_id != user_id:
                return error.error_authorization_fail()

            # 5. ��֤������״̬�Ƿ�Ϊ���ѷ����� (status == "shipped")
            if status != "shipped":
                return error.error_invalid_order_status(order_id)

            # 6. �����������鼮�б�����ÿ�����ҵ����벢�����������
            for book in book_list:
                store_book_id = book['store_book_id']
                quantity = book['quantity']
                price = book['price']
                total_price = quantity * price

                # �� store_book_collection ���ҵ���Ӧ�� store_book_id ��������Ϣ
                store_book = self.store_book_collection.find_one({'_id': store_book_id})
                if not store_book:
                    return error.error_invalid_store_book_id(store_book_id)

                seller_id = store_book['user_id']  # ��ȡ����ID

                # ��֤�����Ƿ����
                if not self.user_id_exist(seller_id):
                    return error.error_non_exist_user_id(seller_id)

                # ���������˻����
                result = self.users_collection.update_one(
                    {"_id": seller_id},
                    {"$inc": {"balance": total_price}}  # �������Ӷ����鼮������
                )
                if result.matched_count == 0:
                    return error.error_non_exist_user_id(seller_id)

            # 7. ���¶���״̬Ϊ�����ջ�������¼�ջ�ʱ��
            self.orders_collection.update_one(
                {"_id": order_id},
                {
                    "$set": {
                        "status": "received",
                        "received_at": datetime.now()  # �����ջ�ʱ��
                    }
                }
            )

        except PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

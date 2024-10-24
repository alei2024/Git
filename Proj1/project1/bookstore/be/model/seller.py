from be.model import error
from be.model import db_conn
import json
from pymongo.errors import PyMongoError
from pymongo import MongoClient, errors  
from datetime import datetime

class Seller(db_conn.DBConn):
    def __init__(self, user_db_name, store_db_name, book_db_name, order_db_name, store_book_db_name,history_orders_db_name):
        super().__init__(user_db_name, store_db_name, book_db_name, order_db_name, store_book_db_name,history_orders_db_name)

    def add_book(self, user_id: str, store_id: str, book_id: str, book_json_str: str, stock_level: int):
        try:
            # ����û����̵��Ƿ����
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            # �� MongoDB �в����鼮
            existing_book = self.books_collection.find_one({'id': book_id})

            if existing_book:  # ����鼮�Ѵ����� books_collection
                # ��ȡ�۸�
                price = existing_book.get("price")
                
                # ����Ϣ���뵽 store_book_collection
                self.store_book_collection.insert_one({
                    'book_id': book_id,
                    'store_id': store_id,
                    'user_id': user_id,
                    'price': price,
                    'stock': stock_level
                })
            else:  
                pass
                '''
                # ����鼮�����ڣ���ȡ�ؼ���Ϣ������ books_collection
                # ��Ҫ�� book_json_str ����ȡ������Ϣ
                
                book_info_json = json.loads(book_json_str)
                price = book_info_json.get("price")

                # �����鼮��Ϣ�� books_collection
                self.books_collection.insert_one(book_info_json)

                # ����Ϣ���뵽 store_book_collection
                self.store_book_collection.insert_one({
                    'book_id': book_id,
                    'store_id': store_id,
                    'user_id': user_id,
                    'price': price,
                    'stock': stock_level
                })
                '''
            self.stores_collection.update_one(
                {'_id': store_id},  # ���Ҷ�Ӧ�� store_id
                {'$push': {'books_list': book_id}}  # �� book_id ׷�ӵ� books_list
            )
    
        except PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"


    def add_stock(self, user_id: str, store_id: str, book_id: str, add_stock: int):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            self.store_book_collection.update_one(
                {"store_id": store_id, "book_id": book_id},
                {"$inc": {"stock": add_stock}}
            )
        except PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str,name: str = None, instruction: str = None) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)

            self.stores_collection.insert_one({
                "_id": store_id,
                "owner_id": user_id,
                "store_name": name if name is not None else "",
                "description": instruction if instruction is not None else "",
                "created_at": datetime.now(),
            })
            self.users_collection.update_one(
                {"_id": user_id},
                {"$push": {"stores": store_id}}
            )
        except PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    #���ҷ���
    def send_books(self, user_id: str, store_id: str, order_id: str):
        try:
            # ��֤�û����̵��Ƿ����
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)

            # ����û��Ƿ�Ϊ�õ��̵�ӵ����
            store = self.stores_collection.find_one({'_id': store_id})
            if store["owner_id"] != user_id:
                return error.error_authorization_fail()

            # ���Ҷ���
            order = self.orders_collection.find_one({'_id': order_id})
            if not order:
                return error.error_invalid_order_id(order_id)
            if order['status'] != "paid":
                return error.error_invalid_order_status(order_id)

            # ���¶���״̬Ϊ "shipped"
            self.orders_collection.update_one(
                {'_id': order_id},
                {"$set": {
                    "status": "shipped",
                    "shipped_at": datetime.now()
                    }}

            )
            
        except PyMongoError as e:
            return 529, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"


'''
    #��ѯ����(�����������ɵĶ���)
    def store_processing_order(self, seller_id):
        try:
            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)

            result = []
            orders = self.mongo['new_order'].find({'store_seller_id': seller_id, 'status': 2})

            for order in orders:
                order_info = {
                    "order_id": order['_id'],
                    "store_id": order['store_id'],
                    "status": order['status'],
                    "total_price": order['total_price'],
                    "order_time": order['order_time']
                }
                books = []
                order_details = self.mongo['new_order_detail'].find({'order_id': order['_id']})
                for book in order_details:
                    books.append({
                        "book_id": book['book_id'],
                        "count": book['count']
                    })
                order_info['books'] = books
                result.append(order_info)

            if not result:
                result = ["NO Processing Order"]

        except PyMongoError as e:
            return 529, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", result

    #��ѯ��ʷ����
    def store_history_order(self, store_id):
        try:
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)

            result = []
            orders = self.mongo['history_order'].find({'store_id': store_id}, {'_id': 0})

            for order in orders:
                result.append(order)

        except PyMongoError as e:
            return 529, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", result
'''
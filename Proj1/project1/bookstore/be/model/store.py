import logging
import os
import pymongo
import threading

# Store�������ݿ�����ķ�װ
class Store:

    def __init__(self):
        # MongoDB����URI�����ݿ�����
        db_url = 'mongodb://localhost:27017/'
        self.client = pymongo.MongoClient(db_url)
        self.db = self.client['be_db']  # MongoDB �е����ݿ���
        self.init_collections()  # ��ʼ������

    # ��������
    def init_collections(self):
        try:
            # �����û�����
            users_collection = self.db.users
            users_collection.create_index("user_id", unique=True)

            # �����̵��鼮����
            store_book_collection = self.db.store_book
            store_book_collection.create_index([("book_id", 1), ("store_id", 1)], unique=True)

            # �����̵꼯��
            stores_collection = self.db.stores
            stores_collection.create_index([("store_id", 1), ("owner_id", 1)], unique=True)

            # ������ǰ��������
            orders_collection = self.db.orders
            orders_collection.create_index("order_id", unique=True)

            # ��ʷ��������
            history_orders_collection = self.db.history_orders
            history_orders_collection.create_index("order_id", unique=True)

            # �鼮���鼯��
            books_collection = self.db.books
            books_collection.create_index("book_id", unique=True)

            logging.info("Collections initialized successfully.")
        except Exception as e:
            logging.error(f"An error occurred while initializing collections: {e}")

def get_db_conn(self):
        return self.client    #����MongoDB�ͻ��˶���

database_instance: Store = None
# global variable for database sync
init_completed_event = threading.Event()
# �������ݿ��ʼ��
def init_database():
    global database_instance
    database_instance = Store()

# �������ݿ�����
def get_db():
    global database_instance
    return database_instance.get_db()




































'''

import logging
import os
import sqlite3 as sqlite
import threading

#Store�������ݿ�����ķ�װ
class Store:
    database: str

    #�����ݿ���и���
    def __init__(self, db_path):
        self.database = os.path.join(db_path, "be.db")#ƴ�����ֲ���ֵ
        self.init_tables()#��ʼ�����
    #������user��user_store��store��new_order��new_order_detai5�����
    def init_tables(self):
        try:
            conn = self.get_db_conn()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS user ("
                "user_id TEXT PRIMARY KEY, password TEXT NOT NULL, "
                "balance INTEGER NOT NULL, token TEXT, terminal TEXT);"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS user_store("
                "user_id TEXT, store_id, PRIMARY KEY(user_id, store_id));"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS store( "
                "store_id TEXT, book_id TEXT, book_info TEXT, stock_level INTEGER,"
                " PRIMARY KEY(store_id, book_id))"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order( "
                "order_id TEXT PRIMARY KEY, user_id TEXT, store_id TEXT)"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order_detail( "
                "order_id TEXT, book_id TEXT, count INTEGER, price INTEGER,  "
                "PRIMARY KEY(order_id, book_id))"
            )

            conn.commit()#�ύ�����Ĳ���
        except sqlite.Error as e:
            logging.error(e)
            conn.rollback()

    def get_db_conn(self) -> sqlite.Connection:
        return sqlite.connect(self.database)

database_instance: Store = None
# global variable for database sync
init_completed_event = threading.Event()

#�������ݿ��ʼ��
def init_database(db_path):
    global database_instance
    database_instance = Store(db_path)

#�������ݿ�����
def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()

    
'''
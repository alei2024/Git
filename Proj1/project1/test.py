import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient, ASCENDING  
from datetime import datetime  
  
# ���ӵ�MongoDB������  
client = MongoClient('localhost', 27017)  
  
# �������ݿ⣨������ǲ����ڵĻ���  
db_users = client['users_db']  
db_stores = client['stores_db']  
db_books = client['books_db']  
db_orders = client['orders_db']  
  
# �������ϣ�MongoDBͨ�����ڲ����һ���ĵ�ʱ�Զ��������ϣ������ǿ�����ʽ������  
users_collection = db_users['users']  
stores_collection = db_stores['stores']  
books_collection = db_books['books']  
orders_collection = db_orders['orders']  
  
# ����ʾ�����ݵ��û�����  
user_data = {  
    "username": "user1",  
    "password": "hashed_password",  # ��ȷ����ʵ��Ӧ���а�ȫ�ش洢����  
    "role": "buyer",  
    "balance": 1000.00,  
    "created_at": datetime.utcnow().isoformat(),  # ʹ�õ�ǰʱ��  
    "stores": [],  
    "orders": []  
}  
users_collection.insert_one(user_data)  
  
# ����ʾ�����ݵ��̵꼯��  
store_data = {  
    "owner_id": users_collection.find_one({"username": "user1"})["_id"],  # ����user1������  
    "store_name": "Bookstore A",  
    "description": "A store for book lovers",  
    "created_at": datetime.utcnow().isoformat(),  
    "books": []  
}  
stores_collection.insert_one(store_data)  
  
# ����ʾ�����ݵ��鼮����  
book_data = {  
    "title": "The Great Gatsby",  
    "author": "F. Scott Fitzgerald",  
    "publisher": "Scribner",  
    "pub_year": "1925",  
    "pages": 180,  
    "price": 15.99,  
    "currency_unit": "USD",  
    "isbn": "9780743273565",  
    "tags": ["classic", "fiction"],  
    "stock": 100,  
    # ������һ��ͼƬ�ֶΣ�����ʡ����ʵ��ͼƬ����  
    "picture": "",  
    "description": "A novel set in the 1920s...",  
    "store_id": stores_collection.find_one()["_id"],  # �������ղŲ�����̵�  
    "created_at": datetime.utcnow().isoformat()  
}  
books_collection.insert_one(book_data)  
  
# ����ʾ�����ݵ���������  
order_data = {  
    "buyer_id": users_collection.find_one({"username": "user1"})["_id"],  
    "store_id": stores_collection.find_one()["_id"],  
    "book_list": [  
        {  
            "book_id": books_collection.find_one()["_id"],  
            "quantity": 1,  
            "price": 15.99  
        }  
    ],  
    "total_price": 15.99,  
    "status": "pending",  
    "created_at": datetime.utcnow().isoformat(),  
    "paid_at": None,  
    "shipped_at": None,  
    "received_at": None  
}  
orders_collection.insert_one(order_data)  
  
# �ر����ӣ���ѡ����Ϊ����ͨ�����ڽű�����ʱ�Զ��رգ�  
client.close()
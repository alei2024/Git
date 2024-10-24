import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient, ASCENDING  
from datetime import datetime  
  
# 连接到MongoDB服务器  
client = MongoClient('localhost', 27017)  
  
# 创建数据库（如果它们不存在的话）  
db_users = client['users_db']  
db_stores = client['stores_db']  
db_books = client['books_db']  
db_orders = client['orders_db']  
  
# 创建集合（MongoDB通常会在插入第一个文档时自动创建集合，但我们可以显式创建）  
users_collection = db_users['users']  
stores_collection = db_stores['stores']  
books_collection = db_books['books']  
orders_collection = db_orders['orders']  
  
# 插入示例数据到用户集合  
user_data = {  
    "username": "user1",  
    "password": "hashed_password",  # 请确保在实际应用中安全地存储密码  
    "role": "buyer",  
    "balance": 1000.00,  
    "created_at": datetime.utcnow().isoformat(),  # 使用当前时间  
    "stores": [],  
    "orders": []  
}  
users_collection.insert_one(user_data)  
  
# 插入示例数据到商店集合  
store_data = {  
    "owner_id": users_collection.find_one({"username": "user1"})["_id"],  # 假设user1是卖家  
    "store_name": "Bookstore A",  
    "description": "A store for book lovers",  
    "created_at": datetime.utcnow().isoformat(),  
    "books": []  
}  
stores_collection.insert_one(store_data)  
  
# 插入示例数据到书籍集合  
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
    # 假设有一个图片字段，这里省略了实际图片数据  
    "picture": "",  
    "description": "A novel set in the 1920s...",  
    "store_id": stores_collection.find_one()["_id"],  # 关联到刚才插入的商店  
    "created_at": datetime.utcnow().isoformat()  
}  
books_collection.insert_one(book_data)  
  
# 插入示例数据到订单集合  
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
  
# 关闭连接（可选，因为连接通常会在脚本结束时自动关闭）  
client.close()
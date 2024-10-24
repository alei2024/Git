from pymongo import MongoClient, ObjectId   
  
class DBConn:
    def __init__(self, user_db_name, store_db_name, book_db_name, order_db_name, store_book_db_name,history_orders_db_name):
        # 连接到MongoDB服务器
        self.client = MongoClient('mongodb://localhost:27017/')
        
        # 获取各个数据库的连接
        self.users_db = self.client[user_db_name]
        self.stores_db = self.client[store_db_name]
        self.books_db = self.client[book_db_name]
        self.orders_db = self.client[order_db_name]
        self.store_book_db = self.client[store_book_db_name]  
        self.history_orders_db = self.client[history_orders_db_name] 
        
        # 获取各个集合的引用
        self.users_collection = self.users_db['users']  # 集合名为'users'
        self.stores_collection = self.stores_db['stores']  # 集合名为'stores'
        self.books_collection = self.books_db['books']  # 集合名为'books'
        self.orders_collection = self.orders_db['orders']  # 集合名为'orders'
        self.store_book_collection = self.store_book_db['store_book']  # 集合'store_book'
        self.history_orders_collection = self.history_orders_db['history_orders']  # 集合'history_orders'
  
    def user_id_exist(self, user_id):  
        #将 user_id 转换为 ObjectId 类型，匹配 MongoDB 中的 ObjectId 类型
        # 检查用户ID是否存在  
        user = self.users_collection.find_one({'_id': ObjectId(user_id)})  
        return user is not None  # 如果找到了文档，则返回 True；否则返回 False 
  
    def store_id_exist(self, store_id):  
        # 检查商店ID是否存在  
        store = self.stores_collection.find_one({'_id': ObjectId(store_id)})  
        return store is not None  
  
    def book_id_exist(self, store_id, book_id):
        # 检查书籍ID是否存在
        # 在 stores 集合中检查 store_id 和 book_id 的存在性
        store = self.stores_collection.find_one(
            {"_id": ObjectId(store_id), "books": ObjectId(book_id)}
        )
        return store is not None
    
    def order_id_exist(self, order_id):  
        # 在 orders 集合中查询 order_id  
        result = self.orders_collection.find_one({'order_id': order_id})   
        return result is not None  



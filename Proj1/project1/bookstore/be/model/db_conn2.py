from pymongo import MongoClient, ObjectId   
  
class DBConn:
    def __init__(self, user_db_name, store_db_name, book_db_name, order_db_name, store_book_db_name,history_orders_db_name):
        # ���ӵ�MongoDB������
        self.client = MongoClient('mongodb://localhost:27017/')
        
        # ��ȡ�������ݿ������
        self.users_db = self.client[user_db_name]
        self.stores_db = self.client[store_db_name]
        self.books_db = self.client[book_db_name]
        self.orders_db = self.client[order_db_name]
        self.store_book_db = self.client[store_book_db_name]  
        self.history_orders_db = self.client[history_orders_db_name] 
        
        # ��ȡ�������ϵ�����
        self.users_collection = self.users_db['users']  # ������Ϊ'users'
        self.stores_collection = self.stores_db['stores']  # ������Ϊ'stores'
        self.books_collection = self.books_db['books']  # ������Ϊ'books'
        self.orders_collection = self.orders_db['orders']  # ������Ϊ'orders'
        self.store_book_collection = self.store_book_db['store_book']  # ����'store_book'
        self.history_orders_collection = self.history_orders_db['history_orders']  # ����'history_orders'
  
    def user_id_exist(self, user_id):  
        #�� user_id ת��Ϊ ObjectId ���ͣ�ƥ�� MongoDB �е� ObjectId ����
        # ����û�ID�Ƿ����  
        user = self.users_collection.find_one({'_id': ObjectId(user_id)})  
        return user is not None  # ����ҵ����ĵ����򷵻� True�����򷵻� False 
  
    def store_id_exist(self, store_id):  
        # ����̵�ID�Ƿ����  
        store = self.stores_collection.find_one({'_id': ObjectId(store_id)})  
        return store is not None  
  
    def book_id_exist(self, store_id, book_id):
        # ����鼮ID�Ƿ����
        # �� stores �����м�� store_id �� book_id �Ĵ�����
        store = self.stores_collection.find_one(
            {"_id": ObjectId(store_id), "books": ObjectId(book_id)}
        )
        return store is not None
    
    def order_id_exist(self, order_id):  
        # �� orders �����в�ѯ order_id  
        result = self.orders_collection.find_one({'order_id': order_id})   
        return result is not None  



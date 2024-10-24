import os  
from pymongo import MongoClient  
import base64  
import json  
from typing import List  

class Book:  
    def __init__(self, data: dict = None):  
        if data:  
            self.id = data.get('_id', '')  
            self.title = data.get('title', '')  
            self.author = data.get('author', '')  
            # ... 其他字段  
            self.tags = data.get('tags', [])  
            self.pictures = data.get('pictures', [])  
        else:  
            self.tags = []  
            self.pictures = []  
  
    def to_dict(self):  
        # 转换 Book 对象为字典，用于保存到 MongoDB  
        return {  
            'title': self.title,  
            'author': self.author,  
            # ... 其他字段  
            'tags': self.tags,  
            'pictures': [base64.b64encode(pic).decode('utf-8') for pic in self.pictures]  
        }  
  
class BookDB:  
    def __init__(self, db_name: str = 'book_db', collection_name: str = 'books'):  
        # 连接到 MongoDB 服务器  
        client = MongoClient('mongodb://localhost:27017/')  
        self.db = client[db_name]  
        self.collection = self.db[collection_name]  
  
    def get_book_count(self):  
        return self.collection.count_documents({})  
  
    def get_book_info(self, start: int, size: int) -> List[Book]:  
        books = []  
        cursor = self.collection.find().sort('id', 1).skip(start).limit(size)  
        for document in cursor:  
            book = Book(data=document)  
            # 注意：这里假设 pictures 字段存储的是字节数组，需要解码为 base64 字符串  
            # 如果 pictures 字段存储的是 base64 字符串，则不需要再次编码  
            # book.pictures = [base64.b64decode(pic).decode('utf-8') if isinstance(pic, str) else pic for pic in book.pictures]  
            # 但由于我们在这里是从 MongoDB 检索数据，所以应该是解码的过程（如果存储的是 base64 字符串）  
            # 然而，由于我们之前可能已经将图片编码为 base64 字符串并存储在 MongoDB 中，  
            # 所以这里我们不需要解码，除非我们打算在代码中直接使用这些图片数据。  
            # 如果只是展示或传输，可以保持 base64 编码形式。  
            books.append(book)  
        return books  
  
# 使用示例  
if __name__ == '__main__':  
    db = BookDB()  
    print(f"Total books: {db.get_book_count()}")  
    books = db.get_book_info(0, 10)  
    for book in books:  
        print(book.title, book.author, book.tags)
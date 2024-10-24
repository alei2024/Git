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
            # ... �����ֶ�  
            self.tags = data.get('tags', [])  
            self.pictures = data.get('pictures', [])  
        else:  
            self.tags = []  
            self.pictures = []  
  
    def to_dict(self):  
        # ת�� Book ����Ϊ�ֵ䣬���ڱ��浽 MongoDB  
        return {  
            'title': self.title,  
            'author': self.author,  
            # ... �����ֶ�  
            'tags': self.tags,  
            'pictures': [base64.b64encode(pic).decode('utf-8') for pic in self.pictures]  
        }  
  
class BookDB:  
    def __init__(self, db_name: str = 'book_db', collection_name: str = 'books'):  
        # ���ӵ� MongoDB ������  
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
            # ע�⣺������� pictures �ֶδ洢�����ֽ����飬��Ҫ����Ϊ base64 �ַ���  
            # ��� pictures �ֶδ洢���� base64 �ַ���������Ҫ�ٴα���  
            # book.pictures = [base64.b64decode(pic).decode('utf-8') if isinstance(pic, str) else pic for pic in book.pictures]  
            # �����������������Ǵ� MongoDB �������ݣ�����Ӧ���ǽ���Ĺ��̣�����洢���� base64 �ַ�����  
            # Ȼ������������֮ǰ�����Ѿ���ͼƬ����Ϊ base64 �ַ������洢�� MongoDB �У�  
            # �����������ǲ���Ҫ���룬�������Ǵ����ڴ�����ֱ��ʹ����ЩͼƬ���ݡ�  
            # ���ֻ��չʾ���䣬���Ա��� base64 ������ʽ��  
            books.append(book)  
        return books  
  
# ʹ��ʾ��  
if __name__ == '__main__':  
    db = BookDB()  
    print(f"Total books: {db.get_book_count()}")  
    books = db.get_book_info(0, 10)  
    for book in books:  
        print(book.title, book.author, book.tags)
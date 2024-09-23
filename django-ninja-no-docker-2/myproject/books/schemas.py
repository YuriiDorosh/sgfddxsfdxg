from ninja import Schema
from datetime import date

class BookSchema(Schema):
    id: int
    title: str
    author: str
    published_date: date
    isbn: str

class BookCreateSchema(Schema):
    title: str
    author: str
    published_date: date
    isbn: str

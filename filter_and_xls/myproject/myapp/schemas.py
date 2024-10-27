from ninja import Schema
from datetime import date
from typing import List

class BookSchema(Schema):
    id: int
    title: str
    publication_date: date

class AuthorSchema(Schema):
    id: int
    name: str
    age: int
    books: List[BookSchema] = []

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

from typing import Any, Generic, TypeVar, Optional, List, Dict

from ninja import Schema
from pydantic import Field

TData = TypeVar('TData')

class ApiResponse(Schema, Generic[TData]):
    data: Optional[TData] = Field(default_factory=dict)
    meta: Dict[str, Any] = Field(default_factory=dict)
    errors: List[Any] = Field(default_factory=list)
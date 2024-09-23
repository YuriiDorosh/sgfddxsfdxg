from ninja_extra import NinjaExtraAPI, api_controller, http_get, http_post, http_put, http_delete
from django.shortcuts import get_object_or_404
from .models import Book
from .schemas import BookSchema, BookCreateSchema
from .permissions import BelongsToAllOrAnyGroupPermission

api = NinjaExtraAPI()

@api_controller('/books', permissions=[BelongsToAllOrAnyGroupPermission(
    all_groups=['group1', 'group2'],
    any_groups=['group3', 'group4']
)])
class BookController:

    @http_get('/')
    def list_books(self, request):
        books = Book.objects.all()
        return [BookSchema.from_orm(book) for book in books]

    @http_post('/')
    def create_book(self, request, payload: BookCreateSchema):
        book = Book.objects.create(**payload.dict())
        return BookSchema.from_orm(book)

    @http_get('/{book_id}')
    def get_book(self, request, book_id: int):
        book = get_object_or_404(Book, id=book_id)
        return BookSchema.from_orm(book)

    @http_put('/{book_id}')
    def update_book(self, request, book_id: int, payload: BookCreateSchema):
        book = get_object_or_404(Book, id=book_id)
        for attr, value in payload.dict().items():
            setattr(book, attr, value)
        book.save()
        return BookSchema.from_orm(book)

    @http_delete('/{book_id}')
    def delete_book(self, request, book_id: int):
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return {"success": True}

api.register_controllers(BookController)

from ninja_extra import NinjaExtraAPI, api_controller, http_get, http_post, http_put, http_delete
from django.shortcuts import get_object_or_404
from .models import Book
from .schemas import BookSchema, BookCreateSchema
from .permissions import CountryGenrePermission

api = NinjaExtraAPI()

@api_controller('/books', permissions=[CountryGenrePermission])
class BookController:

    @http_get('/')
    def list_books(self, request):
        user = request.user
        if user.is_superuser or user.groups.filter(name='special_access').exists():
            # Якщо адміністратор або має спеціальні права, то повертаємо всі книги
            books = Book.objects.all()
        else:
            # Інакше фільтруємо книги за країною і жанром користувача
            books = Book.objects.filter(country=user.profile.country, genre=user.profile.favorite_genre)
        return [BookSchema.from_orm(book) for book in books]

    @http_post('/')
    def create_book(self, request, payload: BookCreateSchema):
        # Користувач може створювати книги тільки своєї країни та жанру
        if request.user.profile.country != payload.country or request.user.profile.favorite_genre != payload.genre:
            return {"error": "You can only create books for your country and favorite genre"}
        book = Book.objects.create(**payload.dict())
        return BookSchema.from_orm(book)

    @http_get('/{book_id}')
    @CountryGenrePermission()
    def get_book(self, request, book_id: int):
        book = get_object_or_404(Book, id=book_id)
        return BookSchema.from_orm(book)

    @http_put('/{book_id}')
    @CountryGenrePermission()
    def update_book(self, request, book_id: int, payload: BookCreateSchema):
        book = get_object_or_404(Book, id=book_id)
        if request.user.profile.country != book.country or request.user.profile.favorite_genre != book.genre:
            return {"error": "You can only edit books from your country and favorite genre"}
        for attr, value in payload.dict().items():
            setattr(book, attr, value)
        book.save()
        return BookSchema.from_orm(book)

    @http_delete('/{book_id}')
    @CountryGenrePermission()
    def delete_book(self, request, book_id: int):
        book = get_object_or_404(Book, id=book_id)
        if request.user.profile.country != book.country or request.user.profile.favorite_genre != book.genre:
            return {"error": "You can only delete books from your country and favorite genre"}
        book.delete()
        return {"success": True}

api.register_controllers(BookController)

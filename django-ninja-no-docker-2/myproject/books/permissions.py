from ninja_extra.permissions import BasePermission
from .models import Book

class CountryGenrePermission(BasePermission):
    def has_permission(self, request, controller, book_id=None):
        user = request.user
        user_country = user.profile.country
        user_genre = user.profile.favorite_genre
        
        # Якщо користувач є адміністратором або має спеціальну групу
        if user.is_superuser or user.groups.filter(name='special_access').exists():
            return True
        
        # Якщо перевіряємо доступ до конкретної книги
        if book_id:
            book = Book.objects.get(id=book_id)
            return book.country == user_country and book.genre == user_genre
        
        # Для загальних запитів, які не стосуються конкретної книги
        return True

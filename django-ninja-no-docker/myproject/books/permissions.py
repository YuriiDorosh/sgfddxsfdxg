# from ninja_extra.permissions import BasePermission

# class BelongsToAllOrAnyGroupPermission(BasePermission):
#     def __init__(self, all_groups=None, any_groups=None):
#         self.all_groups = all_groups or []
#         self.any_groups = any_groups or []

#     def has_permission(self, request, controller):
#         user_groups = set(request.user.groups.values_list('name', flat=True))

#         # Перевірка, чи користувач належить до всіх груп
#         if self.all_groups and all(group in user_groups for group in self.all_groups):
#             return True
        
#         # Перевірка, чи користувач належить хоча б до однієї групи
#         if self.any_groups and any(group in user_groups for group in self.any_groups):
#             return True
        
#         return False


from ninja_extra.permissions import BasePermission
from .models import Book

class BelongsToCountryPermission(BasePermission):
    def has_permission(self, request, controller, book_id=None):
        # Отримуємо країну користувача, наприклад, через request.user.profile.country
        user_country = request.user.profile.country  # передбачимо, що в користувача є поле країни
        
        # Якщо перевірка на рівні одного об'єкта (наприклад, перегляд чи редагування конкретної книги)
        if book_id:
            book = Book.objects.get(id=book_id)
            return book.country == user_country
        
        # Загальний запит, наприклад, на список книг
        return True  # Загальний доступ дозволений, фільтрацію робимо в контролері

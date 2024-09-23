from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    favorite_genre = models.CharField(max_length=100)  # Поле для улюбленого жанру

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)  # Поле для жанру

    class Meta:
        permissions = [
            ("can_view_book", "Can view book"),
        ]

    def __str__(self):
        return self.title

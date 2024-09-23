from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13)
    country = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("can_view_book", "Can view book"),
        ]

    def __str__(self):
        return self.title

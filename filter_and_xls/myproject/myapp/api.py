from ninja_extra import NinjaExtraAPI, api_controller, route
from ninja import File
from ninja.files import UploadedFile
from .models import Author, Book
from typing import List
from .schemas import AuthorSchema, BookSchema
from utils.excel import export_to_excel, import_from_excel

api = NinjaExtraAPI()

@api_controller
class AuthorController:

    @route.get("/list", response=List[AuthorSchema])
    def list_authors(self, request, export: bool = False, include_hidden: bool = False):
        queryset = Author.all_objects.all() if include_hidden else Author.objects.all()

        if export:
            exclude_fields = [] # це щоб всі поля діставались, а не тільки видимі  # TODO TODO TODO TODO TODO TODO 
            # exclude_fields = [] if include_hidden else ['is_hidden']
            return export_to_excel(queryset, exclude_fields=exclude_fields)

        return queryset

    @route.post("/upload", response=dict)
    def upload_authors(self, request, file: UploadedFile = File(...)):
        result = import_from_excel(Author, file.file, exclude_fields=[])
        return result

api.register_controllers(AuthorController)

@api_controller
class BookController:

    @route.get("/list", response=List[BookSchema])
    def list_books(self, request, export: bool = False, include_hidden: bool = False):
        queryset = Book.all_objects.all() if include_hidden else Book.objects.all()

        if export:
            exclude_fields = [] if include_hidden else ['is_hidden']
            return export_to_excel(queryset, exclude_fields=exclude_fields)

        return queryset

    @route.post("/upload", response=dict)
    def upload_books(self, request, file: UploadedFile = File(...)):
        result = import_from_excel(Book, file.file, exclude_fields=[])
        return result

api.register_controllers(BookController)

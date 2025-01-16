from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "website")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date", "is_available")
    list_filter = ("is_available",)
    search_fields = ("title", "author__name")

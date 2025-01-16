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
    actions = ["mark_as_unavailable", "mark_as_available"]

    @admin.action(description="Marcar libros como no disponibles")
    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    @admin.action(description="Marcar libros como disponibles")
    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)

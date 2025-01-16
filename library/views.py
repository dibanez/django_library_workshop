from django.views.generic import ListView, DetailView
from .models import Book, Author


class BookListView(ListView):
    model = Book
    template_name = "library/custom_book_list.html"
    queryset = Book.objects.filter(is_available=True)
    context_object_name = "books"


class BookDetailView(DetailView):
    model = Book


class AuthorListView(ListView):
    model = Author
    context_object_name = "authors"


class AuthorDetailView(DetailView):
    model = Author

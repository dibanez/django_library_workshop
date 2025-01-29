from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from .models import Book, Author
from .serializers import AuthorSerializer, BookListSerializer, BookDetailSerializer


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


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by("name")
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "bio"]
    ordering_fields = ["name"]

    @action(detail=True)
    def books(self, request, pk=None):
        author = self.get_object()
        books = Book.objects.filter(author=author)
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def stats(self, request):
        authors = Author.objects.annotate(
            total_books=Count("book"),
            available_books=Count("book", filter=Q(book__is_available=True)),
        )
        data = [
            {
                "name": author.name,
                "total_books": author.total_books,
                "available_books": author.available_books,
            }
            for author in authors
        ]
        return Response(data)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("title")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "published_date"]

    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return BookListSerializer
        return BookDetailSerializer

    @action(detail=False)
    def available(self, request):
        books = Book.objects.filter(is_available=True)
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def toggle_availability(self, request, pk=None):
        book = self.get_object()
        book.is_available = not book.is_available
        book.save()
        return Response({"status": "success", "is_available": book.is_available})

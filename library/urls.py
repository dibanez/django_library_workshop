from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda request: redirect("book_list", permanent=True)),
    path("books/", views.BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("authors/", views.AuthorListView.as_view(), name="author_list"),
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author_detail"),
]

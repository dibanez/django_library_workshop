from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

router = DefaultRouter()
router.register(r"authors", views.AuthorViewSet)
router.register(r"books", views.BookViewSet)

urlpatterns = [
    path("", lambda request: redirect("book_list", permanent=True)),
    path("books/", views.BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("authors/", views.AuthorListView.as_view(), name="author_list"),
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author_detail"),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

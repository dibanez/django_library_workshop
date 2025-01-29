from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from library.models import Author, Book
from django.contrib.auth.models import User
from datetime import date


class BookAPITests(APITestCase):
    def setUp(self):
        # Create user admin
        self.user = User.objects.create_superuser(
            "admin", "admin@example.com", "admin123"
        )
        self.client.login(username="admin", password="admin123")

        # Create autor
        self.author = Author.objects.create(
            name="Neil Gaiman", bio="Autor británico de fantasía"
        )

        # Create libro
        self.book = Book.objects.create(
            title="American Gods",
            author=self.author,
            published_date=date(2001, 6, 19),
            is_available=True,
        )

    def test_get_books_list(self):
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_book(self):
        data = {
            "title": "Coraline",
            "author": self.author.id,
            "published_date": "2002-07-02",
            "is_available": True,
        }
        response = self.client.post(reverse("book-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

        created_book = Book.objects.get(title="Coraline")
        self.assertEqual(created_book.author, self.author)
        self.assertEqual(str(created_book.published_date), "2002-07-02")
        self.assertTrue(created_book.is_available)

    def test_get_book_detail(self):
        response = self.client.get(reverse("book-detail", args=[self.book.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "American Gods")
        self.assertEqual(response.data["author"], self.author.id)

    def test_update_book(self):
        data = {
            "title": "American Gods - Updated",
            "author": self.author.id,
            "published_date": "2001-06-19",
            "is_available": False,
        }
        response = self.client.put(
            reverse("book-detail", args=[self.book.pk]), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "American Gods - Updated")
        self.assertFalse(self.book.is_available)

    def test_toggle_availability(self):
        url = reverse("book-toggle-availability", args=[self.book.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertFalse(self.book.is_available)

    def test_available_books_filter(self):
        response = self.client.get(reverse("book-available"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

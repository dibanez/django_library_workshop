from django.test import TestCase, Client
from django.urls import reverse
from library.models import Author, Book
from django.contrib.auth.models import User
from datetime import date


class IntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            "admin", "admin@example.com", "admin123"
        )
        self.author = Author.objects.create(
            name="Terry Pratchett", bio="Autor de Mundodisco"
        )
        self.book = Book.objects.create(
            title="El Color de la Magia",
            author=self.author,
            published_date=date(1983, 11, 24),
            is_available=True,
        )

    def test_full_book_workflow(self):
        # 1. Show book list
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El Color de la Magia")

        # 2. Show book detail
        response = self.client.get(reverse("book_detail", args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

        # 3. Verify API
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_full_author_workflow(self):
        # 1. Show author list
        response = self.client.get(reverse("author_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Terry Pratchett")

        # 2. Show author detail
        response = self.client.get(reverse("author_detail", args=[self.author.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.name)

        # 3. Verify API
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse("author-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

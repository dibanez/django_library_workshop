from django.test import TestCase, Client
from django.urls import reverse
from library.models import Author, Book
from datetime import date


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(
            name="Isaac Asimov", bio="Escritor de ciencia ficción"
        )
        self.book = Book.objects.create(
            title="Fundación",
            author=self.author,
            published_date=date(1951, 8, 1),
            is_available=True,
        )

    def test_book_list_view(self):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/custom_book_list.html")
        self.assertContains(response, "Fundación")

    def test_book_detail_view(self):
        response = self.client.get(reverse("book_detail", args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/book_detail.html")
        self.assertContains(response, self.book.title)

    def test_author_list_view(self):
        response = self.client.get(reverse("author_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/author_list.html")
        self.assertContains(response, "Isaac Asimov")

    def test_author_detail_view(self):
        response = self.client.get(reverse("author_detail", args=[self.author.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/author_detail.html")
        self.assertContains(response, self.author.name)

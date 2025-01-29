from django.test import TestCase, Client
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from library.models import Author, Book
from library.admin import AuthorAdmin, BookAdmin


class MockRequest:
    pass


class AdminTest(TestCase):
    def setUp(self):
        # Create superuser
        self.user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123"
        )
        self.client = Client()
        self.client.login(username="admin", password="admin123")

        # Create admin site
        self.site = AdminSite()

        # Create author and books
        self.author = Author.objects.create(
            name="J.K. Rowling", website="https://www.jkrowling.com"
        )

        self.books = [
            Book.objects.create(
                title="Harry Potter 1",
                author=self.author,
                published_date=date(1997, 6, 26),
                is_available=True,
            ),
            Book.objects.create(
                title="Harry Potter 2",
                author=self.author,
                published_date=date(1998, 7, 2),
                is_available=False,
            ),
        ]

    def test_author_admin_list_display(self):
        """Test for the list display of the Author admin"""
        author_admin = AuthorAdmin(Author, self.site)
        self.assertEqual(list(author_admin.list_display), ["name", "website"])

    def test_author_admin_search_fields(self):
        """Test That the author search works"""
        response = self.client.get(
            f"{reverse('admin:library_author_changelist')}?q=Rowling"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "J.K. Rowling")

    def test_author_admin_list_filter(self):
        """Test that the author filters work"""
        response = self.client.get(reverse("admin:library_author_changelist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "By name")

    def test_book_admin_list_display(self):
        """Test for the list display of the Book admin"""
        book_admin = BookAdmin(Book, self.site)
        self.assertEqual(
            list(book_admin.list_display),
            ["title", "author", "published_date", "is_available"],
        )

    def test_book_admin_search_fields(self):
        """Test that the book search works"""
        # Search by title
        response = self.client.get(
            f"{reverse('admin:library_book_changelist')}?q=Harry"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter 1")
        self.assertContains(response, "Harry Potter 2")

        # Search by author
        response = self.client.get(
            f"{reverse('admin:library_book_changelist')}?q=Rowling"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter 1")

    def test_book_admin_list_filter(self):
        """Test that the book filters work"""
        response = self.client.get(
            f"{reverse('admin:library_book_changelist')}?is_available__exact=1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter 1")
        self.assertNotContains(response, "Harry Potter 2")

    def test_book_admin_mark_as_unavailable_action(self):
        """Test the action of marking books as unavailable"""
        # Verify that the book is initially available
        self.assertTrue(self.books[0].is_available)

        # Execute the action
        data = {
            "action": "mark_as_unavailable",
            "_selected_action": [self.books[0].id],
        }
        response = self.client.post(reverse("admin:library_book_changelist"), data)

        # Verify that the book is now unavailable
        self.books[0].refresh_from_db()
        self.assertFalse(self.books[0].is_available)

    def test_book_admin_mark_as_available_action(self):
        """Test the action of marking books as available"""
        # Verify that the book is initially unavailable
        self.assertFalse(self.books[1].is_available)

        # Execute the action
        data = {
            "action": "mark_as_available",
            "_selected_action": [self.books[1].id],
        }
        response = self.client.post(reverse("admin:library_book_changelist"), data)

        # Verify that the book is now available
        self.books[1].refresh_from_db()
        self.assertTrue(self.books[1].is_available)

    def test_bulk_actions(self):
        """Test the bulk actions of the admin"""
        # Create more books
        more_books = [
            Book.objects.create(
                title=f"Book {i}",
                author=self.author,
                published_date=date(2020, 1, 1),
                is_available=True,
            )
            for i in range(3)
        ]

        # Obtain the ids of all available books
        available_book_ids = list(
            Book.objects.filter(is_available=True).values_list("id", flat=True)
        )

        # Check that all books are available
        data = {
            "action": "mark_as_unavailable",
            "_selected_action": available_book_ids,
        }
        self.client.post(reverse("admin:library_book_changelist"), data)

        # Verify that all books are now unavailable
        self.assertEqual(Book.objects.filter(is_available=True).count(), 0)

    def test_admin_permissions(self):
        """Test for admin permissions"""
        # Create a normal user
        normal_user = User.objects.create_user(username="normal", password="normal123")
        client = Client()
        client.login(username="normal", password="normal123")

        # Try to access the admin
        response = client.get(reverse("admin:library_book_changelist"))
        self.assertEqual(response.status_code, 302)  # Redirección por falta de permisos

    def test_admin_change_form(self):
        """Test the change form of the admin"""
        # Try editing a book
        change_url = reverse("admin:library_book_change", args=[self.books[0].id])
        response = self.client.get(change_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter 1")

        # Try editing an author
        change_url = reverse("admin:library_author_change", args=[self.author.id])
        response = self.client.get(change_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "J.K. Rowling")

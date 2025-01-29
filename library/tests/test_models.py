from django.test import TestCase
from datetime import date
from library.models import Author, Book


class AuthorModelTest(TestCase):
    def setUp(self):
        # Create an author for the tests
        self.author = Author.objects.create(
            name="George R.R. Martin",
            bio="Escritor de fantasía épica",
            website="https://www.georgerrmartin.com",
        )

        # Create some books for the author
        self.book1 = Book.objects.create(
            title="Juego de Tronos",
            author=self.author,
            published_date=date(1996, 8, 1),
            is_available=True,
        )

        self.book2 = Book.objects.create(
            title="Choque de Reyes",
            author=self.author,
            published_date=date(1998, 11, 16),
            is_available=False,
        )

        self.recent_book = Book.objects.create(
            title="Vientos de Invierno",
            author=self.author,
            published_date=date(2023, 12, 1),
            is_available=True,
        )

    def test_author_creation(self):
        """Test for basic author creation"""
        self.assertTrue(isinstance(self.author, Author))
        self.assertEqual(str(self.author), "George R.R. Martin")

    def test_author_fields(self):
        """Test the fields of the Author model"""
        self.assertEqual(self.author.name, "George R.R. Martin")
        self.assertEqual(self.author.bio, "Escritor de fantasía épica")
        self.assertEqual(self.author.website, "https://www.georgerrmartin.com")

    def test_get_available_books(self):
        """Test the get_available_books() method"""
        available_books = self.author.get_available_books()
        self.assertEqual(available_books.count(), 2)
        self.assertIn(self.book1, available_books)
        self.assertIn(self.recent_book, available_books)
        self.assertNotIn(self.book2, available_books)

    def test_get_books_count(self):
        """Test the get_books_count() method"""
        self.assertEqual(self.author.get_books_count(), 3)

    def test_author_ordering(self):
        """Test the ordering of authors"""
        Author.objects.create(name="Brandon Sanderson")
        Author.objects.create(name="Patrick Rothfuss")
        authors = Author.objects.all()
        self.assertEqual(authors[0].name, "Brandon Sanderson")
        self.assertEqual(authors[1].name, "George R.R. Martin")
        self.assertEqual(authors[2].name, "Patrick Rothfuss")


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="J.R.R. Tolkien", bio="Creador de la Tierra Media"
        )

        self.old_book = Book.objects.create(
            title="El Hobbit",
            author=self.author,
            published_date=date(1937, 9, 21),
            is_available=True,
        )

        self.recent_book = Book.objects.create(
            title="Cuentos Inconclusos",
            author=self.author,
            published_date=date(2022, 1, 1),
            is_available=True,
        )

    def test_book_creation(self):
        """Test for basic book creation"""
        self.assertTrue(isinstance(self.old_book, Book))
        self.assertEqual(str(self.old_book), "El Hobbit")

    def test_book_fields(self):
        """Test the fields of the Book model"""
        self.assertEqual(self.old_book.title, "El Hobbit")
        self.assertEqual(self.old_book.author, self.author)
        self.assertEqual(self.old_book.published_date, date(1937, 9, 21))
        self.assertTrue(self.old_book.is_available)

    def test_mark_as_unavailable(self):
        """Test the mark_as_unavailable() method"""
        self.assertTrue(self.old_book.is_available)
        self.old_book.mark_as_unavailable()
        self.assertFalse(self.old_book.is_available)

        # Verify that the change was saved to the database
        refreshed_book = Book.objects.get(pk=self.old_book.pk)
        self.assertFalse(refreshed_book.is_available)

    def test_is_recent_property(self):
        """Test the is_recent property"""
        self.assertFalse(self.old_book.is_recent)  # Book from 1937
        self.assertTrue(self.recent_book.is_recent)  # Book from 2022

    def test_book_ordering(self):
        """Test the ordering of books"""
        Book.objects.create(
            title="Silmarillion",
            author=self.author,
            published_date=date(1977, 9, 15),
            is_available=True,
        )
        books = Book.objects.all()
        self.assertEqual(books[0].title, "Cuentos Inconclusos")
        self.assertEqual(books[1].title, "El Hobbit")
        self.assertEqual(books[2].title, "Silmarillion")

    def test_book_author_relationship(self):
        """Test the relationship between books and authors"""
        # Verify that the author has the book
        self.assertIn(self.old_book, self.author.book_set.all())

        # Verify that the book has the author
        self.assertEqual(self.old_book.author.name, "J.R.R. Tolkien")

    def test_cascade_delete(self):
        """Test the cascade delete behavior"""
        book_id = self.old_book.id
        self.author.delete()
        # Verify that the book was deleted
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=book_id)


class ModelIntegrationTest(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name="Isaac Asimov")
        self.author2 = Author.objects.create(name="Arthur C. Clarke")

        self.book1 = Book.objects.create(
            title="Fundación",
            author=self.author1,
            published_date=date(1951, 8, 1),
            is_available=True,
        )

        self.book2 = Book.objects.create(
            title="Segunda Fundación",
            author=self.author1,
            published_date=date(1953, 1, 1),
            is_available=False,
        )

    def test_multiple_authors_and_books(self):
        """Test multiple authors and books"""
        # Verify the number of authors and books
        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(Book.objects.count(), 2)

        # Verify the number of books
        self.assertEqual(self.author1.get_books_count(), 2)
        self.assertEqual(self.author2.get_books_count(), 0)

        # Verify the available books
        self.assertEqual(self.author1.get_available_books().count(), 1)
        self.assertEqual(self.author1.get_available_books().first().title, "Fundación")

    def test_book_availability_changes(self):
        """Test changes in book availability"""
        self.assertEqual(self.author1.get_available_books().count(), 1)

        self.book1.mark_as_unavailable()
        self.assertEqual(self.author1.get_available_books().count(), 0)

        self.book2.is_available = True
        self.book2.save()
        self.assertEqual(self.author1.get_available_books().count(), 1)

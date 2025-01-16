from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, help_text="Breve biografía del autor")
    website = models.URLField(
        blank=True, help_text="Enlace al sitio web oficial del autor"
    )

    def get_available_books(self):
        return self.book_set.filter(is_available=True)

    def get_books_count(self):
        return self.book_set.count()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    is_available = models.BooleanField(default=True)

    def mark_as_unavailable(self):
        self.is_available = False
        self.save()

    @property
    def is_recent(self):
        return self.published_date.year >= 2020

    def __str__(self):
        return self.title

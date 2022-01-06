from django.test import TestCase
from books.models import Book


class BookModelTestCase(TestCase):
    def test_simple_creation(self):
        book = Book.objects.create()
        self.assertIsNotNone(book)


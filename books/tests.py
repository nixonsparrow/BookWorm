from django.test import TestCase
from books.models import Book


class BookModelTestCase(TestCase):
    def setUp(self):
        self.empty_book = Book.objects.create(title='Empty Book', language='pl')

    def test_simple_creation(self):
        book = Book.objects.create()
        self.assertIsNotNone(book)

    def test_book_get_proper_full_language(self):
        self.assertEqual(self.empty_book.get_full_language(), 'Polish')

    def test_if_author_is_blank_not_none(self):
        self.assertIsNotNone(self.empty_book.author)


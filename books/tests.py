from django.test import TestCase
from django.shortcuts import reverse
from books.models import Book
from books.languages import (
    get_language_tags, get_language_names, is_language_name, is_language_tag,
    get_language_tag_from_name, get_language_name_from_tag, get_languages_from_languages_txt
)


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


class LanguageMethodsTestCase(TestCase):
    def test_get_language_tags(self):
        self.assertIn('en', get_language_tags())
        self.assertIn('pl', get_language_tags())

    def test_get_language_names(self):
        self.assertIn('English', get_language_names())
        self.assertNotIn('english', get_language_names())

    def test_is_language_tag(self):
        self.assertTrue(is_language_tag('en'))
        self.assertTrue(is_language_tag('pl'))
        self.assertTrue(is_language_tag('xx'))      # database value for not specified language

    def test_is_language_name(self):
        self.assertTrue(is_language_name('English'))
        self.assertTrue(is_language_name('english'))

    def test_get_language_tag_from_name(self):
        self.assertEqual(get_language_tag_from_name('English'), 'en')
        self.assertEqual(get_language_tag_from_name('english'), 'en')

    def test_get_language_name_from_tag(self):
        self.assertEqual(get_language_name_from_tag('en'), 'English')

    def test_get_languages_from_languages_txt(self):
        self.assertIn(('en', 'English'), get_languages_from_languages_txt())
        self.assertIn(('pl', 'Polish'), get_languages_from_languages_txt())
        self.assertIn(('xx', 'Not specified'), get_languages_from_languages_txt())


class TemplatesUsedTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title='There is no spoon!', author='Neo, Mr. Anderson')

    def test_book_list_uses_proper_templates(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
        self.assertTemplateUsed(response, 'books/book_segment.html')
        self.assertTemplateUsed(response, 'books/search_results.html')
        self.assertTemplateUsed(response, 'books/base.html')

    def test_book_list_search_uses_proper_templates(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/search_results.html')
        self.assertTemplateUsed(response, 'books/book_segment.html')

        self.assertTemplateNotUsed(response, 'books/base.html')

    def test_book_create_uses_proper_templates(self):
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_form.html')
        self.assertTemplateUsed(response, 'books/base.html')

    def test_book_update_uses_proper_templates(self):
        response = self.client.get(reverse('book-update', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_form.html')
        self.assertTemplateUsed(response, 'books/base.html')

    def test_book_delete_uses_proper_templates(self):
        response = self.client.get(reverse('book-delete', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_confirm_delete.html')
        self.assertTemplateUsed(response, 'books/base.html')

    def test_book_import_from_google_uses_proper_templates(self):
        response = self.client.get(reverse('book-import-google'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/import_from_google.html')
        self.assertTemplateUsed(response, 'books/import_from_google_results.html')
        self.assertTemplateUsed(response, 'books/base.html')

    def test_book_import_from_google_results_uses_proper_templates(self):
        response = self.client.get(reverse('google-search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/import_from_google_results.html')

        self.assertTemplateNotUsed(response, 'books/base.html')

    def test_book_api_uses_no_templates(self):
        response = self.client.get(reverse('book-api'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateNotUsed(response, 'books/base.html')

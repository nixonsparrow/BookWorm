from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls.base import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from books.models import Book


class BookFormDeleteTestCase(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

        self.book = Book.objects.create(title='Test', author='Tester', cover_link='http://imnothere.ever',
                                        language='pl', isbn='0987654321098', isbn_10='0987654321', page_count=99)

        self.browser.get(self.live_server_url + reverse('book-update', kwargs={'pk': self.book.id}))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Update book'))

    def tearDown(self):
        self.browser.quit()

    def click_delete_button(self):
        self.browser.find_element(By.ID, 'delete_button').click()
        WebDriverWait(self.browser, 5).until(cond.title_contains('Delete book'))

    def test_template_used(self):
        response = self.client.get(reverse('book-delete', kwargs={'pk': self.book.id}))
        self.assertTemplateUsed(response, 'books/book_confirm_delete.html')

    def test_if_delete_button_redirects(self):
        self.browser.get(self.live_server_url + reverse('book-update', kwargs={'pk': self.book.id}))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Update book'))

        self.click_delete_button()

    def test_if_delete_template_shows_proper_book(self):
        self.browser.get(self.live_server_url + reverse('book-delete', kwargs={'pk': self.book.id}))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Delete book'))

        self.assertIn(self.book.isbn, self.browser.find_element(By.ID, f'book_{self.book.id}_isbn').text)

    def test_if_delete_template_shows_warning(self):
        self.browser.get(self.live_server_url + reverse('book-delete', kwargs={'pk': self.book.id}))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Delete book'))

        self.assertIn('Are you really sure', self.browser.find_element(By.ID, 'warning').text)
        self.assertIn('delete', self.browser.find_element(By.ID, 'warning').text)

    def test_if_able_to_delete_book(self):
        self.browser.get(self.live_server_url + reverse('book-delete', kwargs={'pk': self.book.id}))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Delete book'))

        self.assertIsNotNone(Book.objects.get(id=self.book.id))

        self.browser.find_element(By.ID, 'confirm_delete').click()
        WebDriverWait(self.browser, 5).until(cond.title_contains('Book search'))

        self.assertIsNotNone(Book.objects.filter(id=self.book.id))

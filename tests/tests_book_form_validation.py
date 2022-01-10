from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls.base import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from books.models import Book


class BookCreateFormTestCase(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()

    def open_page_add_book(self):
        self.browser.get(self.live_server_url + reverse('book-create'))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Add book'))

    def fill_the_title_field(self):
        title_field = self.browser.find_element(By.ID, 'id_title')
        title_field.send_keys('Dummy title to check other field')

    def test_is_title_capitalized(self):
        self.open_page_add_book()

        inputbox = self.browser.find_element(By.ID, 'id_title')
        inputbox.send_keys('some title', Keys.ENTER)

        WebDriverWait(self.browser, 5).until(cond.title_contains('Book search'))

        book_id = Book.objects.last().id
        self.assertEqual('Some title', self.browser.find_element(By.ID, f'book_{book_id}_title').text)

    def test_title_field(self):
        self.open_page_add_book()
        title_field = self.browser.find_element(By.ID, 'id_title')

        self.assertIsNotNone(title_field.get_attribute("validationMessage"))
        self.assertIsNotNone(title_field.get_attribute("required"))

        self.fill_the_title_field()
        title_field.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 5).until(cond.title_contains('Book search'))

    def test_title_field_no_double_spaces_or_extra_spaces(self):
        for title in [' Mahatma Gandhi', 'Mahatma  Gandhi', 'Mahatma Gandhi ']:
            self.open_page_add_book()

            inputbox = self.browser.find_element(By.ID, 'id_title')
            inputbox.send_keys(title, Keys.ENTER)

            WebDriverWait(self.browser, 5).until(cond.title_contains('Book search'))

            book_id = Book.objects.last().id
            self.assertEqual('Mahatma Gandhi', self.browser.find_element(By.ID, f'book_{book_id}_title').text)

    def test_author_field_no_double_spaces_or_extra_spaces(self):
        for author in [' Mahatma Gandhi', 'Mahatma  Gandhi', 'Mahatma Gandhi ']:
            self.open_page_add_book()
            self.fill_the_title_field()

            inputbox = self.browser.find_element(By.ID, 'id_author')
            inputbox.send_keys(author, Keys.ENTER)

            WebDriverWait(self.browser, 5).until(cond.title_contains('Book search'))

            book_id = Book.objects.last().id
            self.assertEqual('Mahatma Gandhi', self.browser.find_element(By.ID, f'book_{book_id}_author').text)

    def test_isbn_field_too_short_validation(self):
        self.open_page_add_book()
        self.fill_the_title_field()

        inputbox = self.browser.find_element(By.ID, 'id_isbn')
        inputbox.send_keys('12357', Keys.ENTER)

        WebDriverWait(self.browser, 5).until(cond.presence_of_element_located((By.ID, 'error_1_id_isbn')))
        self.assertIn('exactly 13 digits', self.browser.find_element(By.ID, 'error_1_id_isbn').text)

    def test_isbn_field_only_digits_validation(self):
        self.open_page_add_book()
        self.fill_the_title_field()

        inputbox = self.browser.find_element(By.ID, 'id_isbn')
        inputbox.send_keys('1234567890AAA', Keys.ENTER)

        WebDriverWait(self.browser, 5).until(cond.presence_of_element_located((By.ID, 'error_1_id_isbn')))
        self.assertIn('only use digits', self.browser.find_element(By.ID, 'error_1_id_isbn').text)

        # assert that X as last character is ok
        inputbox = self.browser.find_element(By.ID, 'id_isbn')
        inputbox.clear()
        inputbox.send_keys('123456789012X', Keys.ENTER)

        WebDriverWait(self.browser, 5).until(cond.title_contains('Book search'))

    def test_isbn_10_field_too_short_validation(self):
        self.open_page_add_book()
        self.fill_the_title_field()

        inputbox = self.browser.find_element(By.ID, 'id_isbn_10')
        inputbox.send_keys('12357', Keys.ENTER)

        WebDriverWait(self.browser, 5).until(cond.presence_of_element_located((By.ID, 'error_1_id_isbn_10')))
        self.assertIn('exactly 10 digits', self.browser.find_element(By.ID, 'error_1_id_isbn_10').text)

    def test_isbn_10_field_only_digits_validation(self):
        self.open_page_add_book()
        self.fill_the_title_field()

        inputbox = self.browser.find_element(By.ID, 'id_isbn_10')
        inputbox.send_keys('1234567AAA', Keys.ENTER)

        WebDriverWait(self.browser, 5).until(cond.presence_of_element_located((By.ID, 'error_1_id_isbn_10')))
        self.assertIn('only use digits', self.browser.find_element(By.ID, 'error_1_id_isbn_10').text)

        # assert that X as last character is ok
        inputbox = self.browser.find_element(By.ID, 'id_isbn_10')
        inputbox.clear()
        inputbox.send_keys('123456789X', Keys.ENTER)

        WebDriverWait(self.browser, 5).until(cond.title_contains('Book search'))

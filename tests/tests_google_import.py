from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls.base import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from books.models import Book


class ImportBookTestCase(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()

    def test_google_search_by_author(self):
        self.browser.get(self.live_server_url + reverse('book-import-google'))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Import book'))

        inputbox = self.browser.find_element(By.ID, 'id_google_search_author')
        inputbox.send_keys('Gandhi')

        WebDriverWait(self.browser, 5).until(cond.presence_of_element_located((By.ID, 'book_1')))
        first_result = self.browser.find_element(By.ID, 'book_1_author')
        self.assertIn('Gandhi', first_result.text)

    def test_google_search_by_title(self):
        self.browser.get(self.live_server_url + reverse('book-import-google'))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Import book'))

        inputbox = self.browser.find_element(By.ID, 'id_google_search_title')
        inputbox.send_keys('Gandhi')

        WebDriverWait(self.browser, 5).until(cond.presence_of_element_located((By.ID, 'book_1')))
        first_result = self.browser.find_element(By.ID, 'book_1_title')
        self.assertIn('Gandhi', first_result.text)

    def test_google_search_by_query(self):
        self.browser.get(self.live_server_url + reverse('book-import-google'))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Import book'))

        inputbox = self.browser.find_element(By.ID, 'id_google_search_query')
        inputbox.send_keys('Harry Potter')

        WebDriverWait(self.browser, 5).until(cond.presence_of_element_located((By.ID, 'book_1')))
        first_result = self.browser.find_element(By.ID, 'book_1')
        self.assertIn('harry potter'.lower(), first_result.text.lower())


class AddImportedBookTestCase(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

        self.browser.get(self.live_server_url + reverse('book-import-google'))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Import book'))

        inputbox = self.browser.find_element(By.ID, 'id_google_search_query')
        inputbox.send_keys('Gandhi')

        WebDriverWait(self.browser, 5).until(cond.presence_of_element_located((By.ID, 'book_1')))

    def tearDown(self):
        self.browser.quit()

    def test_add_book_by_import_from_google_method(self):
        new_book_title = self.browser.find_element(By.ID, 'book_1_title').text
        self.browser.find_element(By.ID, 'submit_book_1').click()
        WebDriverWait(self.browser, 5).until(cond.title_contains('Add book'))

        self.browser.find_element(By.ID, 'submit_button').click()
        WebDriverWait(self.browser, 5).until(cond.title_contains('Book search'))

        self.assertEqual(new_book_title, Book.objects.last().title)

from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls.base import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from books.models import Book


def fill_form_with_some_data(browser):
    inputbox = browser.find_element(By.ID, 'id_title')
    inputbox.send_keys('Gandhi')
    inputbox = browser.find_element(By.ID, 'id_author')
    inputbox.send_keys('Gandhi')
    inputbox = browser.find_element(By.ID, 'id_cover_link')
    inputbox.send_keys('https://images-na.ssl-images-amazon.com/images/I/81drR6CSp7S.jpg')
    inputbox = browser.find_element(By.ID, 'id_language')
    inputbox.send_keys('en')
    inputbox = browser.find_element(By.ID, 'id_isbn')
    inputbox.send_keys('123456789012X')
    inputbox = browser.find_element(By.ID, 'id_isbn_10')
    inputbox.send_keys('123456789X')
    inputbox = browser.find_element(By.ID, 'id_page_count')
    inputbox.send_keys(234)


class BookListTestCase(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

        self.book = Book.objects.create(title='Hobbit czyli Tam i z powrotem powraca sobie Sauron z łomotem',
                                        author='John Ronald Reuel Tolkien', language='pl', pub_date='1985-01-01', page_count=233,
                                        cover_link='http://books.google.com/books/content?id=DqLPAAAAMAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api',
                                        )

    def tearDown(self):
        self.browser.quit()

    def test_if_title_is_book_worm(self):
        self.browser.get(self.live_server_url)
        WebDriverWait(self.browser, 5).until(cond.title_contains('Book Worm'))

    def test_if_can_see_book_and_total_count_on_list(self):
        self.browser.get(self.live_server_url)
        WebDriverWait(self.browser, 5).until(cond.presence_of_element_located((By.ID, f'book_{self.book.id}')))

        self.assertIn('Tolkien', self.browser.find_element(By.ID, f'book_{self.book.id}_author').text)
        self.assertIn('Total results: 1', self.browser.find_element(By.ID, 'total_results').text)


class AddBookTestCase(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()

    def open_page_add_book(self):
        self.browser.get(self.live_server_url + reverse('book-create'))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Add book'))

    def test_can_see_add_book_page(self):
        self.open_page_add_book()

    def test_redirect_to_book_list(self):
        self.open_page_add_book()

        inputbox = self.browser.find_element(By.ID, 'id_title')
        inputbox.send_keys('Gandhi', Keys.ENTER)

        WebDriverWait(self.browser, 5).until(cond.title_contains('Book search'))

    def test_can_add_new_book_by_form(self):
        self.open_page_add_book()

        fill_form_with_some_data(self.browser)
        self.browser.find_element(By.ID, 'submit_button').click()

        WebDriverWait(self.browser, 5).until(cond.title_contains('Book search'))

        self.assertIsNotNone(Book.objects.get(title='Gandhi', author='Gandhi', language='en', page_count=234,
                             isbn='123456789012X', isbn_10='123456789X',
                             cover_link='https://images-na.ssl-images-amazon.com/images/I/81drR6CSp7S.jpg'))

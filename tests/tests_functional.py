from django.contrib.staticfiles.testing import LiveServerTestCase, StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls.base import reverse
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from django.test.utils import override_settings
from books.models import Book


class BookListTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

        Book.objects.create(title='Hobbit czyli Tam i z powrotem powraca sobie Sauron z łomotem',
                            author='John Ronald Reuel Tolkien', language='pl', pub_date='1985-01-01', page_count=233,
                            cover_link='http://books.google.com/books/content?id=DqLPAAAAMAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api',
                            )

    def tearDown(self):
        self.browser.quit()

    def test_can_see_book_list(self):
        self.browser.get(self.live_server_url)
        WebDriverWait(self.browser, 5).until(cond.title_contains('Book Worm'))

        self.assertTrue(False, msg='Fix book_form and finish that test')

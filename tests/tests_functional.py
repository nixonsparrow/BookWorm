from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls.base import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
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

    def test_can_see_book_list(self):
        self.browser.get(self.live_server_url + reverse('book-create'))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Book Worm'))

    def test_redirect_to_book_list(self):
        self.browser.get(self.live_server_url + reverse('book-create'))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Book Worm'))

        inputbox = self.browser.find_element(By.ID, 'id_title')
        inputbox.send_keys('Gandhi')
        inputbox.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 5).until(cond.title_contains('Book search'))

    def test_can_add_new_book_by_form(self):
        self.browser.get(self.live_server_url + reverse('book-create'))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Book Worm'))

        fill_form_with_some_data(self.browser)
        self.browser.find_element(By.ID, 'submit_button').click()

        WebDriverWait(self.browser, 5).until(cond.title_contains('Book search'))

        self.assertIsNotNone(Book.objects.get(title='Gandhi', author='Gandhi', language='en', page_count=234,
                             isbn='123456789012X', isbn_10='123456789X',
                             cover_link='https://images-na.ssl-images-amazon.com/images/I/81drR6CSp7S.jpg'))


class BookFormResetButtonTestCase(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()

    def click_reset_button(self):
        self.browser.find_element(By.ID, 'reset_button').click()
        WebDriverWait(self.browser, 5).until(cond.alert_is_present())
        alert = self.browser.switch_to.alert
        alert.accept()

    def test_if_reset_button_has_warning(self):
        self.browser.get(self.live_server_url + reverse('book-create'))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Add book'))

        self.browser.find_element(By.ID, 'reset_button').click()
        WebDriverWait(self.browser, 5).until(cond.alert_is_present())

    def test_if_reset_button_resets_to_clean_form_create_view(self):
        self.browser.get(self.live_server_url + reverse('book-create'))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Add book'))

        fill_form_with_some_data(self.browser)

        ids_to_check = ['id_title', 'id_author', 'id_cover_link', 'id_isbn', 'id_isbn_10', 'id_page_count']

        for id_to_check in ids_to_check:
            self.assertIsNotNone(self.browser.find_element(By.ID, id_to_check).get_attribute('value'))
        self.assertNotEqual('xx', self.browser.find_element(By.ID, 'id_language').get_attribute('value'))

        self.click_reset_button()

        for id_to_check in ids_to_check:
            self.assertFalse(self.browser.find_element(By.ID, id_to_check).get_attribute('value'))
        self.assertEqual('xx', self.browser.find_element(By.ID, 'id_language').get_attribute('value'))

    def test_if_reset_button_resets_to_initial_update_view(self):
        book = Book.objects.create(title='Test', author='Tester', cover_link='http://imnothere.ever', language='pl',
                                   isbn='0987654321098', isbn_10='0987654321', page_count=99)

        self.browser.get(self.live_server_url + reverse('book-update', kwargs={'pk': book.id}))
        WebDriverWait(self.browser, 5).until(cond.title_contains('Update book'))

        form_ids = ['id_title', 'id_author', 'id_cover_link', 'id_isbn', 'id_isbn_10', 'id_page_count']
        for id_to_clear in form_ids:
            self.browser.find_element(By.ID, id_to_clear).clear()

        fill_form_with_some_data(self.browser)

        # check if values in form are DIFFERENT FROM initial ones
        for id_to_check in form_ids:
            if id_to_check in ['id_page_count']:
                form_value = int(self.browser.find_element(By.ID, id_to_check).get_attribute('value'))
            else:
                form_value = self.browser.find_element(By.ID, id_to_check).get_attribute('value')

            self.assertNotEqual(form_value, book.__getattribute__(id_to_check.replace('id_', '')))

        self.click_reset_button()

        # check if values in form are THE SAME AS initial ones
        for id_to_check in form_ids:
            if id_to_check in ['id_page_count']:
                form_value = int(self.browser.find_element(By.ID, id_to_check).get_attribute('value'))
            else:
                form_value = self.browser.find_element(By.ID, id_to_check).get_attribute('value')

            self.assertEqual(form_value, book.__getattribute__(id_to_check.replace('id_', '')))


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

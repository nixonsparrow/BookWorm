from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls.base import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from tests.tests_functional import fill_form_with_some_data
from books.models import Book


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

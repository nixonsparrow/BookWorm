from rest_framework.test import APITestCase
from django.urls import reverse
from books.models import Book


class BooksGETNoFiltersTestCase(APITestCase):
    def test_get_book_empty_list(self):
        response = self.client.get(reverse('book-api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_get_single_book_in_json(self):
        Book.objects.create(title='Test')

        response = self.client.get(reverse('book-api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn("('title', 'Test')", str(response.data))

    def test_get_many_books_in_json(self):
        for nr in range(1, 100):
            Book.objects.create(title=f'Test_{nr}')

        response = self.client.get(reverse('book-api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

        self.assertIn("('title', 'Test_1')", str(response.data))
        self.assertNotIn("('title', 'Test_99')", str(response.data))

        self.assertIsNotNone(Book.objects.filter(title='Test_99').first())


class BooksGETQueryFiltersTestCase(APITestCase):
    authors = ['Tolkien', 'Sapkowski', 'Żeromski', 'Tokarczuk', 'Van Whitespace']
    titles = ['The Hobbit', 'Alice in the Wonderland']
    pub_dates = ['2020-12-31', '1987-06-05', '2020-01-01', '1987-12-12', '2022-01-10']

    def setUp(self):
        for nr in range(5):
            Book.objects.create(title=self.titles[0], author=self.authors[nr], language='en',
                                pub_date=self.pub_dates[nr])

        for nr in range(2):
            Book.objects.create(title=self.titles[1], author=self.authors[nr], language='pl',
                                pub_date=self.pub_dates[nr])
        Book.objects.create(title=self.titles[1], author=self.authors[2], language='en')

    def test_filtering_by_author(self):
        response = self.client.get(reverse('book-api') + f'?inauthor={self.authors[0]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(reverse('book-api') + f'?inauthor={self.authors[4]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(reverse('book-api') + '?inauthor=Author not in sb')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_filtering_by_title(self):
        response = self.client.get(reverse('book-api') + f'?intitle={self.titles[0]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

        response = self.client.get(reverse('book-api') + f'?intitle={self.titles[1]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        response = self.client.get(reverse('book-api') + '?intitle=Title not in db')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_filtering_by_language_tag(self):
        response = self.client.get(reverse('book-api') + '?language=en')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 6)

        response = self.client.get(reverse('book-api') + '?language=pl')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(reverse('book-api') + '?language=wrong')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_filtering_by_language_name(self):
        response = self.client.get(reverse('book-api') + '?language=english')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 6)

        response = self.client.get(reverse('book-api') + '?language=polish')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(reverse('book-api') + '?language=wrong')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_filtering_by_title_and_language(self):
        response = self.client.get(reverse('book-api') + f'?language=pl&intitle={self.titles[1]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(reverse('book-api') + f'?language=en&intitle={self.titles[1]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_filtering_by_date_from(self):
        response = self.client.get(reverse('book-api') + f'?date-from=2000-01-01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_filtering_by_date_to(self):
        response = self.client.get(reverse('book-api') + f'?date-to=2000-01-01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_filtering_by_date_from_and_date_to(self):
        response = self.client.get(reverse('book-api') + f'?date-from=2000-01-01&date-to=2020-12-31')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

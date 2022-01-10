# Book Worm
Manage your books with **Django**, **Heroku**, **Django REST Framework**,
**PostgreSQL**, **htmx** and **Bootstrap**.

## Heroku hosting
Heroku's files are located in the main app folder as ``Procfile`` 
and specifically for Windows ``Procfile.windows``.

## Tests
Unittests are located in a books' app folder:
~~~~
$ books/tests.py
$ tests/api/tests_books_api.py
~~~~
Selenium tests are located in  folder:
~~~~
$ tests/tests_*.py
~~~~

## Details
Settings folder is not named in a Django's default way.
In Book Worm you can find main files like ``settings.py`` at ``/core/`` instead of ``/BookWorm/``.

# Managing book library
## Add a book with form
Go to url (by main site button or directly):
~~~~
/book/new
~~~~
Fill the form with wanted values and click 'Add' button.
## Import a book from Google API
Go to url (by main site button or directly):
~~~~
/book/import
~~~~
Search by title/author or general phrase the book you want to add.
If results are only partly satisfying your expectations,
remember that you can edit in the next step.

Click 'Add to database' button which takes you to the book form.
You can edit the form with wanted values and click 'Add' button.

## Book search
To search for a book that is already in your database,
just enter the main site url:
~~~~
/
~~~~
Searching is dynamic, so if you change the values,
in less than a second results should be updated.
Language choice ``----------`` resets language filter.

Dates ``YYYY-MM-DD`` have to be entered fully to be implemented as a filters.
It's not needed to input both of them to work.

## Book update / delete
To update a book you can simply click on it in search results at the main page.
You can also get url if you know the id of the book you want to edit:
~~~~
/book/<id>
~~~~
The update form is exactly the same as the book creation one.

## Query string search
You can build API to get your books. Just go the url:
~~~~
/api/
~~~~
where ``GET`` method returns all books in database in json format.

You can use same filters here as in ``/`` main page search.
Just add them as query strings following the ``?`` mark to the url.
It's possible to use many in the same time with ``&`` as separator.
Filters:
~~~~
intitle, inauthor, language, date-from, date-to
~~~~
Despite the fact the application returns data in json, you can
also include query string ``format=json`` to get clean json in
a browser if needed.

Usage examples:
~~~~
/api/?intitle=hobbit&inauthor=tolkien&date-to=2000-08-12
/api/?inauthor=tolkien&date-from=2020&language=en
/api/?format=json&date-from=2020&language=en
~~~~
For language tags the applications uses you might go to:
~~~~
$ /books/static/languages.txt
~~~~
but basically they are common language tags with 'xx' as if missing one.
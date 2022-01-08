from django.http import HttpResponseNotFound
from django.shortcuts import render, reverse
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from books.models import Book, get_language_name_from_tag
from books.forms import BookForm, GoogleAPIForm
from django.utils import timezone
import requests


class BooksListView(ListView, FormMixin):

    model = Book
    context_object_name = 'books'
    form_class = BookForm
    template_name = 'books/book_list.html'
    extra_context = {'languages': Book.LANGUAGES,
                     'extra_title': 'Book search',
                     'today': timezone.now().strftime('%Y-%m-%d')}

    def post(self, request, *args, **kwargs):
        data = self.get_form_kwargs()['data']

        title = data['title'].strip()
        author = data['author'].strip()
        language = data['language']
        date_from = data['date-from']
        date_to = data['date-to']

        books = Book.objects.filter(
                title__icontains=title,
                author__icontains=author,
                language__icontains=language
            )

        # due to postgreSQL doesn't support simple gte/lte date filtering, here we have some custom filter
        if any([date_from, date_to]):
            for book in books:
                if date_from and book.pub_date < date_from:
                    books = books.exclude(id=book.id)
                elif date_to and book.pub_date > date_to:
                    books = books.exclude(id=book.id)

        return render(request, self.template_name, context={
            'books': books,
            'title_searched': title,
            'author_searched': author,
            'language_searched': language,
            'date_from_searched': date_from,
            'date_to_searched': date_to
            })


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    extra_context = {'extra_title': 'Add book'}

    def get_initial(self):
        initial = super(BookCreateView, self).get_initial()
        for field in self.request.GET:
            if self.request.GET[field] != 'None':
                initial[field] = self.request.GET[field]
        return initial

    def get_success_url(self):
        return reverse('book-list')


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    extra_context = {'update_form': True,
                     'extra_title': 'Update book'}

    def get_success_url(self):
        return reverse('book-list')


class BookDeleteView(DeleteView):
    model = Book
    context_object_name = 'book'
    extra_context = {'extra_title': 'Delete book'}

    def get_success_url(self):
        return reverse('book-list')


class BookImportFromGoogleView(TemplateView, FormMixin):
    template_name = 'books/import_from_google.html'
    extra_context = {'extra_title': 'Import book'}
    form_class = GoogleAPIForm

    def post(self, request, *args, **kwargs):
        query = self.get_form_kwargs()['data']['google_search_query']
        in_author = self.get_form_kwargs()['data']['google_search_author']
        in_title = self.get_form_kwargs()['data']['google_search_title']

        query_link = f'https://www.googleapis.com/books/v1/volumes?q={query}+'
        query_link += f'intitle:{in_title}+' if in_title else ''
        query_link += f'inauthor:{in_author}+' if in_author else ''

        google_request = requests.get(query_link)

        books = []
        next_id = 1

        if 'items' in google_request.json():
            for google_book in google_request.json()['items']:
                # get those values only if available - otherwise get None
                title = google_book['volumeInfo']['title'] if 'title' in google_book['volumeInfo'] else ''
                author = ', '.join(google_book['volumeInfo']['authors']) if 'authors' in google_book['volumeInfo'] else ''
                pub_date = google_book['volumeInfo']['publishedDate'] if 'publishedDate' in google_book['volumeInfo'] else ''
                page_count = int(google_book['volumeInfo']['pageCount']) if 'pageCount' in google_book['volumeInfo'] else None

                if 'imageLinks' in google_book['volumeInfo']:
                    thumbnail = google_book['volumeInfo']['imageLinks']['thumbnail'] if 'thumbnail' in google_book['volumeInfo']['imageLinks'] else None
                else:
                    thumbnail = None

                isbn, isbn_10 = None, None
                if 'industryIdentifiers' in google_book['volumeInfo']:
                    for identifier in google_book['volumeInfo']['industryIdentifiers']:
                        if identifier['type'] == 'ISBN_13':
                            isbn = identifier['identifier']
                        elif identifier['type'] == 'ISBN_10':
                            isbn_10 = identifier['identifier']

                # Add dummy data to date without day and/or month to fit search queries
                if 0 < len(pub_date):
                    while len(pub_date) < 10:
                        pub_date += '-01'

                language_tag = google_book['volumeInfo']['language']

                books.append({
                    'id': next_id,
                    'title': title,
                    'author': author,
                    'isbn': isbn,
                    'isbn_10': isbn_10,
                    'pub_date': pub_date,
                    'cover_link': thumbnail,
                    'language': language_tag,
                    'get_full_language': get_language_name_from_tag(language_tag),
                    'page_count': page_count
                    })

                next_id += 1

        return render(request, self.template_name, {'google_search_results': books,
                                                    'form': self.get_form()})

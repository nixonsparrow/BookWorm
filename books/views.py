from django.shortcuts import render, reverse
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from books.models import Book
from books.forms import BookForm


class BooksListView(ListView, FormMixin):

    model = Book
    context_object_name = 'books'
    form_class = BookForm
    template_name = 'books/book_list.html'
    extra_context = {'languages': Book.LANGUAGES}

    def post(self, request, *args, **kwargs):
        data = self.get_form_kwargs()['data']

        title = data['title'].strip()
        author = data['author'].strip()
        language = data['language'].strip()
        date_from = data['date-from']
        date_to = data['date-to']

        print(data)
        print(language)

        books = Book.objects.filter(
                title__icontains=title,
                author__icontains=author,
                language__icontains=language
            )

        # due to postgreSQL doesn't support gte/lte date filtering, here we have some custom filter
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


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    extra_context = {'update_form': True}

    def get_success_url(self):
        return reverse('book-list')


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm

    def get_success_url(self):
        return reverse('book-list')


class BookDeleteView(DeleteView):
    model = Book
    context_object_name = 'book'

    def get_success_url(self):
        return reverse('book-list')

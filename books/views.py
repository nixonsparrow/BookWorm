from django.shortcuts import render, reverse
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from books.models import Book
from books.forms import GhostForm


class BooksListView(ListView, FormMixin):

    model = Book
    context_object_name = 'books'
    form_class = GhostForm
    template_name = 'books/book_list.html'

    def post(self, request, *args, **kwargs):
        data = self.get_form_kwargs()['data']

        title = data['title'].replace(' ', '')
        author = data['author'].replace(' ', '')
        language = data['language'].replace(' ', '')
        date_from = data['date-from']
        date_to = data['date-to']

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
            'date_to_searched': date_to,
            })


class BookUpdateView(UpdateView):
    model = Book
    fields = '__all__'
    extra_context = {'update_form': True}

    def get_success_url(self):
        return reverse('book-list')


class BookCreateView(CreateView):
    model = Book
    fields = '__all__'

    def get_success_url(self):
        return reverse('book-list')


class BookDeleteView(DeleteView):
    model = Book
    context_object_name = 'book'

    def get_success_url(self):
        return reverse('book-list')

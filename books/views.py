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

        char_field_values = {'title', 'author', 'language'}

        # clean front white spaces if any
        for char_field, value in data.items():
            if char_field in char_field_values:
                if value:
                    while value[0] == ' ':
                        data[value] = value.replace(' ', '', 1)
                    while value[-1] == ' ':
                        data[value] = value[:-1]

        title = data['title']
        author = data['author']
        language = data['language']
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

        print(data)

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

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, HttpResponse, reverse
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from books.models import Book
from books.forms import SearchForm


class BooksListView(ListView, FormMixin):

    model = Book
    context_object_name = 'books'
    form_class = SearchForm
    template_name = 'books/book_list.html'

    def post(self, request, *args, **kwargs):
        title = self.get_form_kwargs()['data']['title']
        author = self.get_form_kwargs()['data']['author']
        language = self.get_form_kwargs()['data']['language']
        return render(request, self.template_name, context={
            'books': Book.objects.filter(
                title__icontains=title,
                author__icontains=author,
                language__icontains=language
            ),
            'title_searched': title,
            'author_searched': author,
            'language_searched': language
            })

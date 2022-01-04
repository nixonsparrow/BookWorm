from django.urls import path, include
from books.views import BooksListView

urlpatterns = [
    path('', BooksListView.as_view(), name='book-list'),
    path('search/', BooksListView.as_view(template_name='books/search_results.html'), name='search'),
]

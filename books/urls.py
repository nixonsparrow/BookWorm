from django.urls import path, include
from books.views import BooksListView, SearchListView

urlpatterns = [
    path('', BooksListView.as_view(), name='book-list'),
    path('search/', SearchListView.as_view(), name='search'),
]

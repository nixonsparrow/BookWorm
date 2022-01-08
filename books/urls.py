from django.urls import path
from books.views import (
    BooksListView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    BookImportFromGoogleView,
    BookListAPI
)

urlpatterns = [
    path('', BooksListView.as_view(), name='book-list'),
    path('search/', BooksListView.as_view(template_name='books/search_results.html'), name='search'),

    path('book/new', BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>', BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete', BookDeleteView.as_view(), name='book-delete'),

    path('book/import', BookImportFromGoogleView.as_view(), name='book-import-google'),
    path('book/import/search/', BookImportFromGoogleView.as_view(
        template_name='books/import_from_google_results.html'), name='google-search'),

    path('api/', BookListAPI.as_view(), name='book-api')
]

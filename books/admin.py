from django.contrib import admin
from books.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'language', 'pub_date', 'isbn', 'page_count', 'id']


admin.site.register(Book, BookAdmin)

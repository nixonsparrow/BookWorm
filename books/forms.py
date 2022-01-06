from django import forms
from django.core.exceptions import ValidationError
from books.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

from django import forms
from django.core.exceptions import ValidationError
from books.models import Book
import re


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            title = title.capitalize()
        return title

    @classmethod
    def check_isbn_for_validation_errors(cls, number, length):
        if number:
            if len(number) != length:
                raise ValidationError(f"ISBN number should contain exactly {length} digits. (Last character may be X)")

            elif len(re.findall(r'[0-9]+', number[:-1])[0]) != (length - 1):
                raise ValidationError("You may only use digits for ISBN number. (Last character may be X)")

            if number[-1].lower() not in '0123456789x':
                raise ValidationError("Last character has to be either a digit or 'X'.")

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']
        self.check_isbn_for_validation_errors(isbn, 13)

        return isbn

    def clean_isbn_10(self):
        isbn_10 = self.cleaned_data['isbn_10']
        self.check_isbn_for_validation_errors(isbn_10, 10)

        return isbn_10


class GoogleAPIForm(forms.Form):
    class Meta:
        method = "POST"
    google_search_query = forms.CharField(label='Overall', max_length=100, required=False,
                                          widget=forms.TextInput(attrs={'placeholder': 'Search in Google API'}))
    google_search_author = forms.CharField(label='Author', max_length=100, required=False,
                                           widget=forms.TextInput(attrs={'placeholder': 'Search by author'}))
    google_search_title = forms.CharField(label='Title', max_length=100, required=False,
                                          widget=forms.TextInput(attrs={'placeholder': 'Search by title'}))

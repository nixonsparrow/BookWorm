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
            title = title[0].capitalize() + title[1:]
        return title

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']
        if isbn:
            if len(isbn) != 13:
                raise ValidationError("ISBN number should contain exactly 13 digits. (Last character may be X)")

            elif len(re.findall(r'[0-9]+', isbn[:-1])[0]) != 12:
                raise ValidationError("You may only use digits for ISBN number. (Last character may be X)")

            if isbn[-1].lower() not in '0123456789x':
                raise ValidationError("Last character has to be either a digit or 'X'.")

        return isbn

    def clean_isbn_10(self):
        isbn_10 = self.cleaned_data['isbn_10']
        if isbn_10:
            if len(isbn_10) != 10:
                raise ValidationError("ISBN-10 number should contain exactly 10 digits. (Last character may be X)")

            elif len(re.findall(r'[0-9]+', isbn_10[:-1])[0]) != 9:
                raise ValidationError("You may only use digits for ISBN-10 number. (Last character may be X)")

            if isbn_10[-1].lower() not in '0123456789x':
                raise ValidationError("Last character has to be either a digit or 'X'.")

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

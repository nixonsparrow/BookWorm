from django import forms
from django.core.exceptions import ValidationError
from books.models import Book
import re


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def clean_isbn(self):
        data = self.cleaned_data['isbn']
        if data:
            if len(data) != 13:
                raise ValidationError("ISBN number should contain exactly 13 digits.")

            elif len(re.findall(r'[0-9]+', data)[0]) != 13:
                raise ValidationError("You may only use digits for ISBN number.")

        return data

    def clean_isbn_10(self):
        data = self.cleaned_data['isbn_10']
        if data:
            if len(data) != 10:
                raise ValidationError("ISBN-10 number should contain exactly 10 digits.")

            elif len(re.findall(r'[0-9]+', data)[0]) != 10:
                raise ValidationError("You may only use digits for ISBN-10 number.")

        return data


class GoogleAPIForm(forms.Form):
    google_search_author = forms.CharField(label='Author', max_length=100, required=False,
                                           widget=forms.TextInput(attrs={'placeholder': 'Search by author'}))
    google_search_title = forms.CharField(label='Title', max_length=100, required=False,
                                          widget=forms.TextInput(attrs={'placeholder': 'Search by title'}))

from langcodes import standardize_tag, Language, LanguageTagError
from django.db import models


class Book(models.Model):
    class Meta:
        ordering = ['title']

    title = models.CharField('Title', max_length=100, default='', null=False, blank=False)
    author = models.CharField('Author', max_length=100, default='', null=True, blank=True)
    cover_link = models.CharField('Link to the cover', default='', max_length=150, null=True, blank=True)
    language = models.CharField('Language', default='', max_length=10, null=True, blank=True)

    pub_date = models.DateField('Publication Date', default=None, null=True, blank=True)

    isbn = models.CharField('ISBN', max_length=13, default='', null=True, blank=True)
    isbn_10 = models.CharField('ISBN 10', max_length=10, default='', null=True, blank=True)
    page_count = models.IntegerField('Pages', default=None, null=True, blank=True)

    def get_full_language_from_tag(self):
        try:
            tag = standardize_tag(str(self.language))
            return Language.make(language=tag).display_name()
        except LanguageTagError:
            pass

        return False

    def get_full_language(self):
        if self.get_full_language_from_tag():
            return self.get_full_language_from_tag()

        return str(self.language).capitalize()

    def __str__(self):
        return f'{self.title}{" (" + str(self.author) + ")" if self.author else ""}'

from django.db import models


class Book(models.Model):
    title = models.CharField('Title', max_length=100, default='', null=True, blank=True)
    author = models.CharField('Author', max_length=100, default='', null=True, blank=True)
    cover_link = models.CharField('Link to the cover', default='', max_length=150)
    language = models.CharField('Language', default='', max_length=100)

    isbn = models.CharField('ISBN', max_length=13, default='', null=True, blank=True)
    isbn_10 = models.CharField('Old ISBN', max_length=10, default='', null=True, blank=True)

    pub_date = models.DateField('Publication Date', default=None)
    pages = models.IntegerField('Pages', default=0)

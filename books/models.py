from django.db import models


def get_languages_from_languages_txt():
    # returns list of tuples (TAG, LANGUAGE) i.e. ('pl', 'Polish')
    return [tuple(row[2:-2].split("', '")) for row in list(map(str, open('books/static/languages.txt').read().split('\n')))]


def get_language_name_from_tag(the_tag):
    try:
        return [name for tag, name in Book.LANGUAGES if tag == the_tag][0]
    except IndexError:
        return None


class Book(models.Model):
    class Meta:
        ordering = ['title']

    LANGUAGES = get_languages_from_languages_txt()

    title = models.CharField('Title', max_length=100, default='', null=False, blank=False)
    author = models.CharField('Author', max_length=100, default='', null=False, blank=True)
    cover_link = models.CharField('Link to the cover', default='', max_length=150, null=True, blank=True)
    language = models.CharField('Language', default=LANGUAGES[0], max_length=10, null=False, blank=False,
                                choices=LANGUAGES)

    pub_date = models.DateField('Publication Date', default=None, null=True, blank=True)

    isbn = models.CharField('ISBN', max_length=13, default='', null=True, blank=True, unique=True)
    isbn_10 = models.CharField('ISBN 10', max_length=10, default='', null=True, blank=True, unique=True)
    page_count = models.IntegerField('Pages', default=None, null=True, blank=True)

    def get_full_language(self):
        return get_language_name_from_tag(self.language)

    def __str__(self):
        return f'{self.title}{" (" + str(self.author) + ")" if self.author else ""}'


if __name__ == '__main__':
    print(get_languages_from_languages_txt())


def get_languages_from_languages_txt():
    # returns list of tuples (TAG, LANGUAGE) i.e. [('pl', 'Polish'), ('en', 'English')]
    return [tuple(row[2:-2].split("', '")) for row in list(map(str, open('books/static/languages.txt').read().split('\n')))]


def get_language_tags():
    return (tag for tag, language in get_languages_from_languages_txt())


def get_language_names(lowercase=False):
    if lowercase:
        return (language.lower() for tag, language in get_languages_from_languages_txt())
    return (language for tag, language in get_languages_from_languages_txt())


def is_language_tag(tag):
    return tag in get_language_tags()


def is_language_name(tag):
    return tag.lower() in get_language_names(lowercase=True)


def get_language_name_from_tag(the_tag):
    try:
        return [name for tag, name in get_languages_from_languages_txt() if tag == the_tag][0]
    except IndexError:
        return None


def get_language_tag_from_name(lang_name):
    try:
        return [tag for tag, name in get_languages_from_languages_txt() if name.lower() == lang_name.lower()][0]
    except IndexError:
        return None

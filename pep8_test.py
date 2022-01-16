import os


folders = [
    'books/',
    'core/',
    'staticfiles/',
    'tests/',
    'templates/',
    'manage.py',
]

if __name__ == '__main__':
    for folder in folders:
        os.system(f'pycodestyle {folder}')

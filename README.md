# BookMingle

A blind dating app for books that accepts user keywords or themes and returns a list of book descriptions (but no covers, titles, or authors) that match those keywords. When a user selects a book to "date", the cover and title are revealed. The app merges user-generated data from the Goodreads, LibraryThing, and Amazon book APIs, along with the Words API to find synonyms and parts of speech when generating the book descriptions.

## To Run

1. Clone the repo.
2. From the command line, cd into the root directory (wherever the manage.py file is located).
3. Type ```python manage.py runserver``` into the command line.
4. Open a web browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
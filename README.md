# Book Guise

My app will suggest new books to read by allowing the user to input a title of a known favorite book and suggesting similar works. The resulting list of books will be presented with no cover, title, or author; instead each suggested book will have its own list of keywords or (as a stretch goal) an automatically generated description of the book as if the description is a posting on a dating website.

Example: Frankenstein might have as its keywords, “gothic,” “victorian,” “horror,” “science fiction,” etc. If I’m able to implement the stretch goal of automatically generated book descriptions, the book’s description might read, “I like to wear a lot of black. I can be very formal in public but you know there are interesting things happening behind closed doors. Suitors must relish the unseemly and face grotesquery without fear.”

The app merges user-generated data from the Goodreads and LibraryThing APIs, and uses Django and Python.

## To Run

1. Clone the repo.
2. From the command line, cd into the root directory (wherever the manage.py file is located).
3. Type ```python manage.py runserver``` into the command line.
4. Open a web browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
import requests
from django.shortcuts import render
from bookguise.fave_book_search import fave_book
from bookguise.suggested_book_builder import Suggested_Book


def fave_book_search(request):
    fave_result = []

    if request.method == 'POST':
        title_input = request.POST['title_input'].strip()

        if title_input:
            fave_result = fave_book(title_input)
            suggested_books = list()

            if not isinstance(fave_result, str):
                for book in fave_result["similar_titles"]:
                    suggested_book_result = Suggested_Book(book)
                    suggested_books.append(suggested_book_result)
                print(suggested_books)

    return render(request, 'bookguise/index.html', {'fave_result': fave_result, 'suggested_books': suggested_books})

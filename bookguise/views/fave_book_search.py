import requests
from django.shortcuts import render
from bookguise.fave_book_search import find_fave
from bookguise.suggested_book_builder import Suggested_Book


def fave_book_search(request):
    # context = RequestContext(request)
    fave_result = []

    if request.method == 'POST':
        title_input = request.POST['title_input'].strip()

        if title_input:
            fave_result = find_fave(title_input)
            suggested_books = list()
            for book in fave_result["similar_titles"]:
                suggested_book_result = Suggested_Book(book)
                suggested_books.append(suggested_book_result)
            print(suggested_books)

    return render(request, 'bookguise/index.html', {'fave_result': fave_result, 'suggested_books': suggested_books})

import requests
from django.shortcuts import render
from bookguise.fave_book_search import find_fave
from bookguise.suggested_book_builder import Suggested_Book


def fave_book_search(request):
    fave_result = []

    if request.method == 'POST':
        title_input = request.POST['title_input'].strip()

        if title_input:
            fave_result = find_fave(title_input)
            suggested_books = list()

            if not isinstance(fave_result, str):
                for book in fave_result["similar_titles"]:
                    search_counter = 0
                    if search_counter < 3:
                        suggested_book_result = Suggested_Book(book)
                        suggested_books.append(suggested_book_result)
                        search_counter += 1
                print(suggested_books)

    return render(request, 'bookguise/index.html', {'fave_result': fave_result, 'suggested_books': suggested_books})

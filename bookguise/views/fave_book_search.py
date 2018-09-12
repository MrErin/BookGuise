import requests
from django.shortcuts import render_to_response
from django.template import RequestContext
from bookguise.fave_book_search import find_fave
from bookguise.suggested_book_builder import build_suggested_book


def fave_book_search(request):
    context = RequestContext(request)
    fave_result = []

    if request.method == 'POST':
        title_input = request.POST['title_input'].strip()

        if title_input:
            fave_result = find_fave(title_input)
            for book in fave_result["similar_titles"]:
                suggested_book_result = build_suggested_book(book)
                print(suggested_book_result)

    return render_to_response('bookguise/index.html', {'fave_result': fave_result}, context)
    # ! Steve says need to bind suggested book result somehow into the context here.

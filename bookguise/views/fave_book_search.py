import requests
from bookguise.fave_book_search import find_fave
from django.shortcuts import render_to_response
from django.template import RequestContext


def fave_book_search(request):
    context = RequestContext(request)
    fave_result = []

    if request.method == 'POST':
        title_input = request.POST['title_input'].strip()

        if title_input:
            fave_result = find_fave(title_input)

    return render_to_response('bookguise/index.html', {'fave_result': fave_result}, context)

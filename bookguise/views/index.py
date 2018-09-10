from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('This is the BookGuise Index')
    # return render(request, 'index.html')

from django.urls import path
from . import views

app_name = "bookguise"
urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.fave_book_search, name='fave_book_search')
]

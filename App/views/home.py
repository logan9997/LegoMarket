from django.shortcuts import render, HttpResponse
from django.core.handlers.wsgi import WSGIRequest

TEMPLATE_URL = 'App/home/home.html'
TITLE = 'Home'

def home(request:WSGIRequest) -> None:

    context = {
        'title': TITLE
    }
    return render(request, TEMPLATE_URL, context=context)
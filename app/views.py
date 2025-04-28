from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'app/home.html')


def categories(request: HttpRequest) -> HttpResponse:
    return render(request, 'app/categories.html')

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView, DetailView


class PostcardHome(ListView):
    template_name = 'index.html'
    title_page = 'Магазин открыток'

    def get_queryset(self):
        return self.queryset


class ShowPostcard(DetailView):
    template_name = 'postcard.html'
    slug_url_kwarg = 'postcard_slug'


class PostcardCategory(ListView):
    template_name = 'index.html'


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
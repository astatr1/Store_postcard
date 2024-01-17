from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, Postcard


def postcard_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    postcards = Postcard.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        postcards = postcards.filter(category=category)
    return render(request, 'store/postcard/list.html',
                  {'category': category,
                   'categories': categories,
                   'postcards': postcards})


def postcard_detail(request, slug):
    postcard = get_object_or_404(Postcard, slug=slug, available=True)
    return render(request, 'store/postcard/detail.html',
                  {'postcard': postcard})


# class PostcardCategory(ListView):
#     template_name = 'index.html'


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
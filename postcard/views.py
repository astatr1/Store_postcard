from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import Category, Postcard
from basket.forms import BasketAddPostcardForm
from .recommender import Recommender


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
    basket_postcard_form = BasketAddPostcardForm()
    r = Recommender()
    recommended_postcards = r.offer_postcard_for([postcard], 3)
    return render(request, 'store/postcard/detail.html',
                  {'postcard': postcard,
                   'basket_postcard_form': basket_postcard_form,
                   'recommended_postcards': recommended_postcards})


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
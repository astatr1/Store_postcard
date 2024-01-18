from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from postcard.models import Postcard
from .basket import Basket
from .forms import BasketAddPostcardForm


@require_POST
def basket_add(request, postcard_id):
    basket = Basket(request)
    postcard = get_object_or_404(Postcard, id=postcard_id)
    form = BasketAddPostcardForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        basket.add(postcard=postcard, quantity=cd['quantity'],
                   override_quantity=cd['override'])
    return redirect('basket:basket_detail')


@require_POST
def basket_remove(request, postcard_id):
    basket = Basket(request)
    postcard = get_object_or_404(Postcard, id=postcard_id)
    basket.remove(postcard)
    return redirect('basket:basket_detail')


def basket_detail(request):
    basket = Basket(request)
    return render(request, 'basket/detail.html',
                  {'basket': basket})

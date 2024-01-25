from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from basket.basket import Basket
from .tasks import order_created


def order_create(request):
    basket = Basket(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if basket.coupon:
                order.coupon = basket.coupon
                order.discount = basket.coupon.discount
            order.save()
            for item in basket:
                OrderItem.objects.create(order=order, postcard=item['postcard'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            basket.clear()  # После записи всех позиций в БД, корзина очищается
            order_created.delay(order.id)  # Запуск асинхронного задания по отправке email
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html',
                  {'basket': basket, 'form': form})


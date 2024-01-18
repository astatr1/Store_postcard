from decimal import Decimal
from django.conf import settings
from postcard.models import Postcard


class Basket:
    def __init__(self, request):
        """Инициализация корзины."""
        self.session = request.session
        basket = self.session.get(settings.CART_SESSION_ID)
        if not basket:
            basket = self.session[settings.CART_SESSION_ID] = {}
        self.basket = basket

    def add(self, postcard, quantity=1, override_quantity=False):
        """Добавить товар в корзину либо обновить количество"""
        postcard_id = str(postcard.id)
        if postcard_id not in self.basket:
            self.basket[postcard_id] = {'quantity': 0, 'price': str(postcard.price)}
        if override_quantity:
            self.basket[postcard_id]['quantity'] = quantity
        else:
            self.basket[postcard_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, postcard):
        """Удаление товара из корзины"""
        postcard_id = str(postcard.id)
        if postcard_id in self.basket:
            del self.basket[postcard_id]
            self.save()

    def __iter__(self):
        """Прокрутка товаров в корзине и получение их из БД"""
        postcard_ids = self.basket.keys()
        postcards = Postcard.objects.filter(id__in=postcard_ids)
        basket = self.basket.copy()
        for postcard in postcards:
            basket[str(postcard.id)]['postcard'] = postcard
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчет количества всех товаров в корзине"""
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        """Получение общей стоимости товаров в корзине"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

    def clear(self):
        """Удаление корзины из сеанса"""
        del self.basket[settings.CART_SESSION_ID]
        self.save()
        
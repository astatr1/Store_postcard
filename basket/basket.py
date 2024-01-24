from decimal import Decimal
from django.conf import settings
from postcard.models import Postcard
from coupons.models import Coupon


class Basket:
    def __init__(self, request):
        """Инициализация корзины."""
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket
        # Сохранение текущего примененного купона
        self.coupon_id = self.session.get('coupon_id')

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
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
            return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) \
                * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
        
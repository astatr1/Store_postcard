from celery import shared_task
from django.core.mail import send_mail
from .models import Order
import os
from dotenv import load_dotenv

load_dotenv()


@shared_task
def order_created(order_id):
    """Задание для отправки уведомления по электронной почте
    при успешном создании заказа"""
    order = Order.objects.get(id=order_id)
    subject = f'Номер заказа {order.id}'
    message = f'Уважаемый (-ая) {order.first_name}, ' \
        f'Вы успешно оформили заказ.'\
        f'Ваш номер заказа {order.id}.'
    mail_sent = send_mail(subject, message, os.getenv('EMAIL_HOST'),
                          [order.email])
    return mail_sent

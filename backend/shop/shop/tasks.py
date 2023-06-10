from decimal import Decimal

from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail as django_send_mail

from dotenv import load_dotenv

import requests

from .models import Book, Order


load_dotenv()


@shared_task
def send_mail(subject, message, from_email, to_email):
    django_send_mail(subject, message, from_email, to_email)


@shared_task
def books_sync():
    r = requests.get('http://store:8001/books/')
    books_data = r.json()

    book_ids_in_data = [book_data['id'] for book_data in books_data]

    books_in_db = Book.objects.exclude(id_in_store__in=book_ids_in_data)
    books_in_db.delete()

    for book_data in books_data:
        book, _ = Book.objects.update_or_create(
            id_in_store=book_data['id'],
            defaults={
                'title': book_data['title'],
                'price': Decimal(book_data['price']),
                'quantity': int(book_data['quantity'])
            }
        )


@shared_task
def orders_sync():
    r = requests.get('http://store:8001/orders/')
    orders_data = r.json()

    for order_data in orders_data:
        order = Order.objects.get(id=order_data['order_id_in_shop'])

        if order.status != order_data['status']:
            subject = 'Your order status was changed!'
            message = 'Check the status of your orders in "My orders" tab.'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [order.user.email, ]
            send_mail.delay(subject, message, from_email, to_email)

        order, _ = Order.objects.update_or_create(
            id=order_data['order_id_in_shop'],
            defaults={'status': order_data['status']}
        )

from decimal import Decimal

from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.urls import reverse_lazy

from dotenv import load_dotenv

import requests

from .models import Book, Order


load_dotenv()


@shared_task
def send_mail(subject, message, from_email, to_email):
    django_send_mail(subject, message, from_email, to_email)


@shared_task
def books_sync():
    full_books_data = []

    next_page = True
    page = 'http://store:8001/books/?page=1'

    while next_page:
        r = requests.get(page)
        books_data = r.json()

        if books_data['next']:
            page_number = books_data['next'][-1]
            page = f'http://store:8001/books/?page={page_number}'
        else:
            next_page = False

        full_books_data.extend(books_data['results'])

    book_ids_in_data = [book_data['id'] for book_data in full_books_data]

    books_in_db = Book.objects.exclude(id_in_store__in=book_ids_in_data)
    books_in_db.delete()

    for book_data in full_books_data:
        book, _ = Book.objects.update_or_create(
            id_in_store=book_data['id'],
            defaults={
                'title': book_data['title'],
                'price': Decimal(book_data['price']),
                'quantity': int(book_data['quantity']),
                'description': book_data['description']
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
            message = f'Check the status of your orders in "My orders" tab: {settings.DOMAIN}{reverse_lazy("shop:my_orders")}'  # noqa
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [order.user.email, ]
            send_mail.delay(subject, message, from_email, to_email)

        order, _ = Order.objects.update_or_create(
            id=order_data['order_id_in_shop'],
            defaults={'status': order_data['status']}
        )

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
    page = 1

    while next_page:
        r = requests.get(f'http://store:8001/books/?page={page}')
        books_data = r.json()

        if books_data.get('next'):
            page += 1
        else:
            next_page = False

        full_books_data.extend(books_data['results'])

    book_ids_in_data = [book_data['id'] for book_data in full_books_data]

    books_in_db = Book.objects.exclude(id_in_store__in=book_ids_in_data)
    books_in_db.delete()

    for book_data in full_books_data:
        img_url = book_data.get('image')
        if img_url:
            image_url = img_url.replace('http://store:8001', settings.API_DOMAIN)
        else:
            image_url = None

        book, _ = Book.objects.update_or_create(
            id_in_store=book_data['id'],
            defaults={
                'title': book_data['title'],
                'price': Decimal(book_data['price']),
                'quantity': int(book_data['quantity']),
                'description': book_data.get('description'),
                'image': image_url
            }
        )


@shared_task
def successful_orders_sync():
    full_successful_orders_data = []

    next_page = True
    page = 1

    while next_page:
        r = requests.get(f'http://store:8001/orders/?status=success&page={page}')
        successful_orders_data = r.json()

        if successful_orders_data.get('next'):
            page += 1
        else:
            next_page = False

        full_successful_orders_data.extend(successful_orders_data['results'])

    order_ids_in_shop = [order_data['order_id_in_shop'] for order_data in full_successful_orders_data]

    orders_to_update_and_email = Order.objects.filter(id__in=order_ids_in_shop).exclude(status=Order.SUCCESS)

    for order_to_update in orders_to_update_and_email:
        subject = 'Your order succeeded!'
        message = f'Check the status of your orders in "My orders" tab: {settings.DOMAIN}{reverse_lazy("shop:my_orders")}'  # noqa
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [order_to_update.user.email, ]

        send_mail.delay(subject, message, from_email, to_email)

    orders_to_update_and_email.update(status=Order.SUCCESS)


@shared_task
def failed_orders_sync():
    full_failed_orders_data = []

    next_page = True
    page = 1

    while next_page:
        r = requests.get(f'http://store:8001/orders/?status=fail&page={page}')
        failed_orders_data = r.json()

        if failed_orders_data.get('next'):
            page += 1
        else:
            next_page = False

        full_failed_orders_data.extend(failed_orders_data['results'])

    order_ids_in_shop = [order_data['order_id_in_shop'] for order_data in full_failed_orders_data]

    orders_to_update_and_email = Order.objects.filter(id__in=order_ids_in_shop).exclude(status=Order.FAIL)

    for order_to_update in orders_to_update_and_email:
        subject = "We are sorry, but we couldn't process your order!"
        message = f'Check the status of your orders in "My orders" tab: {settings.DOMAIN}{reverse_lazy("shop:my_orders")}'  # noqa
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [order_to_update.user.email, ]

        send_mail.delay(subject, message, from_email, to_email)

    orders_to_update_and_email.update(status=Order.FAIL)

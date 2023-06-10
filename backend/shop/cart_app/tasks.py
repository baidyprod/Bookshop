import os

from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail as django_send_mail

import requests

from shop.models import Book


@shared_task
def send_mail(subject, message, from_email, to_email):
    django_send_mail(subject, message, from_email, to_email)


@shared_task
def create_order_in_api(data):
    headers = {
        'Authorization': f'Token {os.getenv("TOKEN")}',
        'Content-Type': 'application/json'
    }

    order_json = {
        'user_email': data['user_email'],
        'delivery_address': data['delivery_address'],
        'order_id_in_shop': data['order_id_in_shop']
    }

    order_post = requests.post('http://store:8001/orders/', headers=headers, json=order_json)

    order_items_json = [{'order': order_post.json()["id"], 'book': k, 'quantity': v}
                        for k, v in data['order_items'].items()]

    order_items_post = requests.post('http://store:8001/orderitems/', headers=headers, json=order_items_json)  # noqa

    subject = 'You have successfully created an order!'
    message = f'''Here are your order details:\nItems:\n{', '.join(f"{Book.objects.get(id_in_store=k).title}: {v}" for k, v in data['order_items'].items())}\nDelivery address: {data['delivery_address']}'''  # noqa
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [data['user_email'], ]
    send_mail.delay(subject, message, from_email, to_email)

import os

from dotenv import load_dotenv

from decimal import Decimal

from celery import shared_task

import requests

from .models import Book


load_dotenv()


@shared_task
def books_sync():
    r = requests.get('http://store:8001/books/')
    books_data = r.json()

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

    order_items_json = [{'order_id': order_post.json()["id"], 'book_id': k, 'quantity': v}
                        for k, v in data['order_items'].items()]

    order_items_post = requests.post('http://store:8001/orderitems/', headers=headers, json=order_items_json)

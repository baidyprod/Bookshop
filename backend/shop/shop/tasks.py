from decimal import Decimal

from celery import shared_task

import requests

from .models import Book


@shared_task
def books_sync():
    r = requests.get('http://store:8001/books/')
    books_data = r.json()

    Book.objects.all().delete()

    books = []
    for book_data in books_data:
        book = Book(
            id_in_store=book_data['id'],
            title=book_data['title'],
            price=Decimal(book_data['price']),
            quantity=int(book_data['quantity'])
        )
        books.append(book)

    Book.objects.bulk_create(books)

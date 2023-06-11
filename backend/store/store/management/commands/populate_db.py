from decimal import Decimal
from random import randint

from django.core.management.base import BaseCommand

from store.models import Book, BookItem


class Command(BaseCommand):
    help = 'Create books and book items'

    def handle(self, *args, **options):
        books = []
        book_items = []

        for i in range(50):
            book_name = f'Book {i+1}'
            description = f'This is description for Book {i+1}'

            book = Book(title=book_name, price=Decimal(randint(10, 100)), description=description)
            books.append(book)

            num_items = randint(0, 5)

            for j in range(num_items):
                place = f'Place {j+1}'

                book_item = BookItem(book=book, place=place)
                book_items.append(book_item)

        Book.objects.bulk_create(books)
        BookItem.objects.bulk_create(book_items)

        self.stdout.write(self.style.SUCCESS('Books and book items created successfully.'))

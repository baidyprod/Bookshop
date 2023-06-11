from django.core.management.base import BaseCommand

from store.models import Book, BookItem, Order, OrderItem, OrderItemBookItem


class Command(BaseCommand):
    help = 'Clears all instances of Book, Order, and OrderItem models.'

    def handle(self, *args, **options):
        Book.objects.all().delete()
        BookItem.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
        OrderItemBookItem.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('All store models cleared successfully.'))

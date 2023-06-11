from django.core.management.base import BaseCommand

from shop.models import Book, Order, OrderItem


class Command(BaseCommand):
    help = 'Clears all instances of Book, Order, and OrderItem models.'

    def handle(self, *args, **options):
        Book.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('All shop models cleared successfully.'))

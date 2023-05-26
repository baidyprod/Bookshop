from django.db import models


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Book(AbstractBaseModel):
    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title


class BookItem(AbstractBaseModel):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    place = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Book Item'
        verbose_name_plural = 'Book Items'

    def __str__(self):
        return self.book_id.title


class Order(AbstractBaseModel):
    STATUS_CHOICES = (
        ('in_work', 'In Work'),
        ('success', 'Success'),
        ('fail', 'Fail'),
    )

    user_email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='in_work')
    delivery_address = models.CharField(max_length=100)
    order_id_in_shop = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(AbstractBaseModel):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'


class OrderItemBookItem(AbstractBaseModel):
    order_item_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    book_item_id = models.ForeignKey(BookItem, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Order Item Book Item'
        verbose_name_plural = 'Order Item Book Items'

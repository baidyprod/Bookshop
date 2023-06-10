from django.db import models


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Book(CreatedAtMixin):
    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title


class Order(CreatedAtMixin):
    IN_WORK = 'in_work'
    SUCCESS = 'success'
    FAIL = 'fail'

    STATUS_CHOICES = (
        (IN_WORK, 'In Work'),
        (SUCCESS, 'Success'),
        (FAIL, 'Fail'),
    )

    user_email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='in_work')
    delivery_address = models.CharField(max_length=100)
    order_id_in_shop = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(CreatedAtMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"Order #{self.order.pk} - Item: {self.book.title}"

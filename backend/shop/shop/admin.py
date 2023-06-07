from django.contrib import admin

from .models import Book, Order, OrderItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'quantity']
    list_per_page = 20
    search_fields = ['title', ]
    list_filter = ['price', 'quantity']
    list_editable = ['price', ]
    readonly_fields = ['pk', ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass

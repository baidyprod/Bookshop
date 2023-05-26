from django.contrib import admin

from store.models import Book, BookItem, Order, OrderItem, OrderItemBookItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    list_per_page = 20
    search_fields = ['title', ]
    list_filter = ['price', ]
    list_editable = ['price', ]


@admin.register(BookItem)
class BookItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['book_id', ]
    list_display = ['get_book_title', 'place']
    list_per_page = 20
    search_fields = ['place', ]

    def get_book_title(self, obj):
        return obj.book_id.title

    get_book_title.short_description = 'Book Title'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItemBookItem)
class OrderItemBookItemAdmin(admin.ModelAdmin):
    pass

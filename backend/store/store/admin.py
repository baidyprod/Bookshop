from django.contrib import admin

from store.models import Book, BookItem, Order, OrderItem, OrderItemBookItem


class BookItemInline(admin.TabularInline):
    model = BookItem
    extra = 0


class OrderItemBookItemInline(admin.TabularInline):
    model = OrderItemBookItem
    extra = 0
    autocomplete_fields = ['book_item', ]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class PriceListFilter(admin.SimpleListFilter):
    title = 'Price'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return [
            ('0-10', 'Less than $10'),
            ('10-50', 'Between $10 and $50'),
            ('50-100', 'Between $50 and $100'),
            ('100', 'Greater than $100'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0-10':
            return queryset.filter(price__lt=10)
        if self.value() == '10-50':
            return queryset.filter(price__gte=10, price__lt=50)
        if self.value() == '50-100':
            return queryset.filter(price__gte=50, price__lt=100)
        if self.value() == '100':
            return queryset.filter(price__gte=100)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'quantity']
    list_per_page = 20
    search_fields = ['title', ]
    list_editable = ['price', ]
    list_filter = [PriceListFilter, ]
    sortable_by = ['price', 'quantity']
    inlines = [BookItemInline, ]

    def quantity(self, obj):
        return obj.bookitem_set.count()


@admin.register(BookItem)
class BookItemAdmin(admin.ModelAdmin):
    list_display = ['book', 'place']
    list_per_page = 20
    search_fields = ['book__title', ]

    def book(self, obj):
        return obj.book.title

    book.admin_order_field = 'book__title'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user_email', 'status', 'created_at']
    list_filter = ['status']
    readonly_fields = ['created_at']
    search_fields = ['user_email', ]
    inlines = [OrderItemInline, OrderItemBookItemInline]
#
#
# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['order', 'book', 'quantity']
#
#     def book(self, obj):
#         return obj.book.title
#
#     book.admin_order_field = 'book__title'

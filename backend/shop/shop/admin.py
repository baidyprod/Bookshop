from django.contrib import admin

from .models import Book, Order, OrderItem


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


class QuantityListFilter(admin.SimpleListFilter):
    title = 'Availability'
    parameter_name = 'quantity'

    def lookups(self, request, model_admin):
        return [
            ('0', 'Not available'),
            ('gt0', 'Available'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(quantity=0)
        if self.value() == 'gt0':
            return queryset.filter(quantity__gt=0)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'quantity']
    list_per_page = 20
    search_fields = ['title', ]
    list_filter = [PriceListFilter, QuantityListFilter]
    list_editable = ['price', ]
    readonly_fields = ['pk', ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'status', 'created_at']
    list_filter = ['status']
    readonly_fields = ['created_at']
    inlines = [OrderItemInline, ]

    def user(self, obj):
        return obj.user.username

    user.admin_order_field = 'user__username'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity']
    list_filter = ['order']

    def book(self, obj):
        return obj.book.title

    book.admin_order_field = 'book__title'

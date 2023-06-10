from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.views import generic

from shop.forms import BookSearchForm, PriceFilterForm
from shop.models import Book, Order, OrderItem

User = get_user_model()


class BookList(generic.ListView):
    model = Book
    template_name = 'shop/home.html'
    context_object_name = 'books'
    paginate_by = 20
    ordering = ['title']

    def get_queryset(self):
        queryset = super().get_queryset()
        form = PriceFilterForm(self.request.GET)
        if form.is_valid():
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']

            if min_price and max_price:
                queryset = queryset.filter(price__gte=min_price, price__lte=max_price).order_by('title')
            elif min_price:
                queryset = queryset.filter(price__gte=min_price)
            elif max_price:
                queryset = queryset.filter(price__lte=max_price)

        search_form = BookSearchForm(self.request.GET)
        if search_form.is_valid() and search_form.cleaned_data['search_query']:
            search_query = search_form.cleaned_data['search_query']
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PriceFilterForm(self.request.GET)
        context['search_form'] = BookSearchForm(self.request.GET)
        return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'shop/book_detail.html'
    context_object_name = 'book'
    pk_url_kwarg = 'pk'


class OrderList(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'shop/my_orders.html'
    context_object_name = 'orders'
    ordering = ['-created_at', ]
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context['orders']

        prefetch_order_items = Prefetch(
            'orderitem_set',
            queryset=OrderItem.objects.select_related('book'),
            to_attr='order_items'
        )
        orders = orders.prefetch_related(prefetch_order_items)

        context['orders'] = orders
        return context

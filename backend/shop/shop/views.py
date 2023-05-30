from urllib.parse import urlencode

from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views import generic

from shop.custom_cart import CustomCart
from shop.forms import BookSearchForm, ModifiedUserCreationForm, PriceFilterForm
from shop.models import Book

User = get_user_model()


class Register(SuccessMessageMixin, generic.FormView):
    template_name = 'registration/register.html'
    form_class = ModifiedUserCreationForm
    success_url = reverse_lazy("home")
    success_message = 'Successfully registered, welcome!'

    def form_valid(self, form):
        user = form.save()
        user = authenticate(username=user.username, password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super(Register, self).form_valid(form)


class UserProfile(generic.DetailView):
    model = User
    template_name = "registration/profile.html"
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        username = self.kwargs.get(self.slug_url_kwarg)
        user = get_object_or_404(User, username=username)
        return user


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


@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = CustomCart(request)
    product = Book.objects.get(id=id)
    cart.add(product=product)
    redirect_url = f"{reverse('home')}?{request.GET.urlencode()}"
    return redirect(redirect_url)


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = CustomCart(request)
    product = Book.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = CustomCart(request)
    product = Book.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = CustomCart(request)
    product = Book.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = CustomCart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

from urllib.parse import urlencode

from cart_app.custom_cart import CustomCart
from cart_app.forms import UserAddressForm
from cart_app.tasks import create_order_in_api as celery_create_order

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy

from shop.models import Book, Order, OrderItem


@login_required(login_url=reverse_lazy('login'))
def cart_add(request, id):
    cart = CustomCart(request)
    product = Book.objects.get(id=id)
    cart.add(product=product)
    redirect_url = f"{reverse('shop:home')}?{request.GET.urlencode()}"
    return redirect(redirect_url)


@login_required(login_url=reverse_lazy('login'))
def item_clear(request, id):
    cart = CustomCart(request)
    product = Book.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_app:cart_detail")


@login_required(login_url=reverse_lazy('login'))
def item_increment(request, id):
    cart = CustomCart(request)
    product = Book.objects.get(id=id)
    cart.add(product=product)
    cart_items = request.session.get('cart')
    quantity = cart_items[f'{id}']['quantity']
    return JsonResponse({'quantity': quantity})


@login_required(login_url=reverse_lazy('login'))
def item_decrement(request, id):
    cart = CustomCart(request)
    product = Book.objects.get(id=id)
    cart.decrement(product=product)
    cart_items = request.session.get('cart')
    quantity = cart_items[f'{id}']['quantity']
    return JsonResponse({'quantity': quantity})


@login_required(login_url=reverse_lazy('login'))
def cart_clear(request):
    cart = CustomCart(request)
    cart.clear()
    return redirect("cart_app:cart_detail")


@login_required(login_url=reverse_lazy('login'))
def cart_detail_and_create_order(request):
    if request.method == 'POST':
        user_address_form = UserAddressForm(request.POST)
        cart = CustomCart(request)

        if user_address_form.is_valid():
            delivery_address = user_address_form.cleaned_data['delivery_address']

            if delivery_address:
                order_items = []
                order_items_dict = {}
                order = Order(user=request.user, delivery_address=delivery_address)

                for key, value in request.session.get('cart').items():
                    book = get_object_or_404(Book, id=key)
                    quantity_requested = value['quantity']

                    if quantity_requested > book.quantity:
                        messages.error(request, f"Cannot create order: {quantity_requested} {book.title} items are "
                                                f"temporary unavailable. Please try again later.")
                        return redirect('cart_detail')

                    order_items.append(OrderItem(order=order, book=book, quantity=quantity_requested))
                    order_items_dict[book.id_in_store] = quantity_requested

                order.save()
                OrderItem.objects.bulk_create(order_items)
                data = {
                    'user_email': request.user.email,
                    'delivery_address': delivery_address,
                    'order_id_in_shop': order.pk,
                    'order_items': order_items_dict
                }
                celery_create_order.delay(data)
                messages.success(request, "Order created successfully.")
                cart.clear()
                return redirect('shop:home')

            else:
                messages.error(request, "Cannot create order: Delivery address is empty.")
                return redirect('cart_app:cart_detail')
        else:
            messages.error(request, "Cannot create order: Invalid form data.")
            return redirect('cart_app:cart_detail')

    else:
        user_address_form = UserAddressForm()

    context = {'user_address_form': user_address_form}
    return render(request, 'cart/cart_detail.html', context)

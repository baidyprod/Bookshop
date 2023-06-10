from django.urls import path

from .views import cart_add, cart_clear, cart_detail_and_create_order, item_clear, item_decrement, item_increment

app_name = 'cart_app'

urlpatterns = [
    path('add/<int:id>/', cart_add, name='cart_add'),
    path('item_clear/<int:id>/', item_clear, name='item_clear'),
    path('item_increment/<int:id>/', item_increment, name='item_increment'),
    path('item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart_clear/', cart_clear, name='cart_clear'),
    path('cart_detail/', cart_detail_and_create_order, name='cart_detail'),
]

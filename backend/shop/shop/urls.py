from django.urls import path

from .views import BookList, OrderList

app_name = 'shop'

urlpatterns = [
    path('', BookList.as_view(), name='home'),
    path("my_orders/", OrderList.as_view(), name="my_orders"),

]

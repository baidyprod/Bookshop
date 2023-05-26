from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from rest_framework.authtoken import views

from store.views import BookItemViewSet, BookViewSet, OrderItemBookItemViewSet, OrderItemViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'bookitems', BookItemViewSet, basename='bookitem')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'orderitems', OrderItemViewSet, basename='orderitem')
router.register(r'orderitembookitems', OrderItemBookItemViewSet, basename='orderitembookitem')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.ObtainAuthToken.as_view()),
    path('', include(router.urls)),
]

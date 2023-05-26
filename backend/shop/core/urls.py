from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from shop.views import BookList, Register, UserProfile

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', BookList.as_view(), name='home'),

    path("accounts/", include('django.contrib.auth.urls')),
    path("accounts/register/", Register.as_view(), name="register"),

    path("profile/<str:username>/", UserProfile.as_view(), name="profile"),


]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

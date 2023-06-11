from django.urls import include, path

from .views import Register, UserProfile

app_name = 'accounts'

urlpatterns = [
    path("", include('django.contrib.auth.urls')),
    path("register/", Register.as_view(), name="register"),
    path("user/<str:username>/", UserProfile.as_view(), name="profile"),

]

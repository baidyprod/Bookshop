from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from shop.forms import ModifiedUserCreationForm
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

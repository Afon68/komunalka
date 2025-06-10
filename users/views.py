from re import A, L
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.core.cache import cache
from django.db.models import Prefetch
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from django.views.generic import CreateView, TemplateView, UpdateView
# from traitlets import Instance
from django.db import connection, reset_queries
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login

from apartaments.models import Apartment
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin

class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
   

    def get_success_url(self):
        print(f"self.request.POST={self.request.POST}")
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse('user:logout'):
            # if redirect_page and is_safe_url(redirect_page, allowed_hosts={self.request.get_host()}) and redirect_page != reverse_lazy('user:logout'):
            return redirect_page
        return reverse_lazy("users:profile")

    def form_valid(self, form):
        print(f"request={self.request}")
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            messages.success(
                self.request,
                f"{user.username}, Вы успешно вошли в аккаунт",
            )
            print(f"user={user}")
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Aвторизация"
        return context

class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("user:profile")

    def form_valid(self, form):
        
        user = form.instance
        print(f"user={user}")

        if user:
            form.save()
            auth.login(self.request, user)
            messages.success(self.request, f"{user.username}, Вы успешно зарегистрировались и вошли в аккаунт")

        return HttpResponseRedirect(self.success_url)
     

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Регистрация"
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("user:profile") 

    def get_object(self, queryset=None):
        return self.request.user 

    

    def form_valid(self, form):
        user = form.save(commit=False)
        # print("image:", user.image)  #  для отладки
        user.save()
        messages.success(self.request, "Профайл успешно обновлен")
        return redirect(self.success_url)


    def form_invalid(self, form):
        messages.error(self.request, "Профайл не обновлен")
        return super().form_invalid(form) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        apartments = Apartment.objects.filter(user=user)
        context["title"] = "Home - Кабинет"
        context["apartments"] = apartments
        
        return context 


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы успешно вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse("main:index"))

@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы успешно вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse("main:index"))



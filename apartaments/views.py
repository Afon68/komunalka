from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from apartaments.forms import ApartmentForm
from .models import Apartment
from django.contrib.auth.mixins import LoginRequiredMixin


def add_apartment(request):
    if request.method == "POST":
        form = ApartmentForm(request.POST)
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.user = request.user
            apartment.save()
            messages.success(request, "Конфигурация услуг квартиры успешно сохранена.")
            return redirect("apartaments:user_objects")
    else:
        form = ApartmentForm()

    return render(
        request,
        "apartaments/add_apartment.html",
        {"form": form, "title": "Добавить квартиру"},
    )


class AddApartmentView(TemplateView):
    template_name = 'apartaments/add_apartment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить квартиру'
        return context


class UserObjectsView(LoginRequiredMixin, TemplateView):
    template_name = 'apartaments/user_objects.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        apartments = Apartment.objects.filter(user=user)
        context["apartments"] = apartments
        context['title'] = 'Мои квартиры'
        return context

def del_apartment(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id, user=request.user)

    if request.method == "POST":
        apartment.delete()
        messages.success(request, "Квартира успешно удалена.")
        return redirect(reverse("apartaments:user_objects"))

    # Показываем подтверждение, если GET
    return render(request, "apartaments/confirm_delete.html", {"apartment": apartment})


def apartment_profile(request, apartment_id):
   
    apartment = get_object_or_404(Apartment, id=apartment_id, user=request.user)
   
    return render(
        request, "apartaments/apartment_profile.html", {"apartment": apartment, "title": "Профиль квартиры", "apartment_id": apartment_id}
    )


def edit_apartment(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id, user=request.user)

    if request.method == "POST":
        form = ApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            form.save()
            messages.success(request, "Изменения успешно сохранены.")
            return redirect("apartaments:apartment_profile", apartment_id=apartment.id)
    else:
        form = ApartmentForm(instance=apartment)

    return render(
        request,
        "apartaments/edit_apartment.html",
        {"form": form, "apartment": apartment, "title": "Редактировать профиль квартиры"},
    )

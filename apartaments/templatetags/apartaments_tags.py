from os import name
from re import A
from django import template
from django.shortcuts import get_object_or_404
from regex import F

from apartaments.models import Apartment


register = template.Library()

@register.simple_tag()
def apartaments_tags(request, apartment_id):
    if request.user and apartment_id:
        apartment = get_object_or_404(Apartment, id=apartment_id, user=request.user) #get_object_or_404(Apartment, id=apartment_id, user=request.user)
        list_verbose_name = ["Все услуги"]
        for field in apartment._meta.fields:
            if field.verbose_name in [
                "Газ.",
                "Доставка газа.",
                
                "Электричество.",
                "Лифт.",
                "Вывоз мусора.",
                "Квартплата.",
                "Интернет.",
                "Домофон.",
                "Центральное отопление.",
            ]:
               
                value = getattr(apartment, field.name)
                

                if value is True or (isinstance(value, int) and not isinstance(value, bool) and value >= 0):
                    list_verbose_name.append(field.verbose_name)

        return list_verbose_name
   
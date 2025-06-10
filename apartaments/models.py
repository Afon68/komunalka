from django.db import models

from users.models import User 

class Apartment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Пользователь")
    timestamp = models.DateTimeField(null=True,auto_now_add=True, verbose_name="Дата и время")
    apartment_name = models.CharField(max_length=200,unique=True,verbose_name="Название квартиры")
    has_gas = models.PositiveIntegerField( null=True, verbose_name="Газ")
    has_gas_delivery = models.BooleanField(default=False, verbose_name="Доставка газа")
    has_water = models.PositiveIntegerField( null=True, verbose_name="Вода.")
    has_hot_water = models.PositiveIntegerField( null=True, verbose_name="Горячая вода")
    has_electricity = models.PositiveIntegerField( null=True, verbose_name="Электричество")
    uses_lift = models.BooleanField(default=False, verbose_name="Лифт")
    has_garbage = models.BooleanField(default=False, verbose_name="Вывоз мусора")
    has_apart_payment = models.BooleanField(default=False, verbose_name="Квартплата")
    has_internet = models.BooleanField(default=False, verbose_name="Интернет")
    has_intercom = models.BooleanField(default=False, verbose_name="Домофон")
    has_heating = models.BooleanField(default=False, verbose_name="Центральное отопление")
    area_apartment = models.PositiveIntegerField(null=True,blank=True, verbose_name="Площадь квартиры")
    number_registered = models.PositiveIntegerField(null=True,blank=True,verbose_name="Количество зарегистрированных в квартире")
    has_water_abon_plata = models.BooleanField(default=False, verbose_name="Абонплата за воду")

    class Meta:
        db_table = "Apartments"
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"
        ordering = ("id",)

    def __str__(self):
        return f"{self.apartment_name} | {self.user.username}"



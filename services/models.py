from django.db import models

from apartaments.models import Apartment

class GasIndicators(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")
    apartment = models.ForeignKey(to=Apartment, on_delete=models.CASCADE, verbose_name='Пользователь')
    gas_meter = models.DecimalField(null=True, max_digits=8, decimal_places=2, verbose_name="Показания газ.счётчика" )
    gas_tariff_counter = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на газ по счётчику")
    gas_tariff_no_counter = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на газ без счётчика")
    gas_delivery = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="Доставка газа")
    number_registered_snapshot = models.PositiveIntegerField(null=True, blank=True, verbose_name="Количество зарегистрированных в квартире")

    class Meta:
        db_table = "Gas"
        verbose_name = "Газ"
        verbose_name_plural = "Газ"
        ordering = ("id",)

    def __str__(self):
        return f"Gas {self.apartment.apartment_name}"


class WaterIndicators(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")
    apartment = models.ForeignKey(to=Apartment, on_delete=models.CASCADE, verbose_name='Пользователь')
    water_meter_one = models.DecimalField(null=True, max_digits=8, decimal_places=2, verbose_name="Показания вод.счётчика")
    water_meter_two = models.DecimalField(null=True, max_digits=8, decimal_places=2, verbose_name="Показания вод.счётчика #2")
    water_tariff_counter = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на воду по счётчику")
    water_tariff_nocounter = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на воду без счётчика")
    water_abon_plata = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="aбонплата на воду")
    number_registered_snapshot = models.PositiveIntegerField(null=True, blank=True, verbose_name="Количество зарегистрированных в квартире")

    class Meta:
        db_table = "Water"
        verbose_name = "Вода"
        verbose_name_plural = "Вода"
        ordering = ("id",)

    def __str__(self):
        return f"Water {self.apartment.apartment_name}"


class HotWaterIndicators(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")
    apartment = models.ForeignKey(to=Apartment, on_delete=models.CASCADE, verbose_name='Пользователь')
    hot_water_meter = models.DecimalField(null=True, max_digits=8, decimal_places=2, verbose_name="Показания счётчика горячей воды")
    hot_water_tariff_counter = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на горячую воду по счётчику")
    hot_water_tariff_no_counter = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на горячую воду без счётчика")
    heating_tariff_counter = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на нагрев воды со счётчиком")
    heating_tariff_no_counter = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на нагрев воды без счётчика")
    number_registered_snapshot = models.PositiveIntegerField(null=True, blank=True, verbose_name="Количество зарегистрированных в квартире")

    class Meta:
        db_table = "HotWater"
        verbose_name = "Горячая вода"
        verbose_name_plural = "Горячая вода"
        ordering = ("id",)

    def __str__(self):
        return f"HotWater {self.apartment.apartment_name}"

class ElectricityIndicators(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")
    apartment = models.ForeignKey(to=Apartment, on_delete=models.CASCADE, verbose_name='Пользователь')
    electro_meter_one = models.DecimalField(null=True, max_digits=8, decimal_places=2, verbose_name="Показания электр.счётчика-1")
    electro_tariff_one = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на электроэнергию-1")
    electro_meter_two = models.DecimalField(null=True, max_digits=8, decimal_places=2, verbose_name="Показания электр.счётчика - 2")
    electro_tariff_two = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на электроэнергию - 2")
    electro_power_apartment = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="Электрическая мощность квартиры")
    electro_tariff_no_counter = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на электроэнергию без счётчика ")


    class Meta:
        db_table = "Еlectricity"
        verbose_name = "Электроэнергия"
        verbose_name_plural = "Электроэнергия"
        ordering = ("id",)

    def __str__(self):
        return f"Electricity {self.apartment.apartment_name}"

class OtherPayments(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")
    apartment = models.ForeignKey(to=Apartment, on_delete=models.CASCADE, verbose_name='Пользователь')   
    tariff_apart_payment = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на квартплату")
    tariff_garbage = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на вывоз мусора") 
    tariff_lift = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на лифт")
    tariff_heating = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="тариф на отопление")
    internet = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="платеж за интернет")
    intercom = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="платеж за домофон")
    number_registered_snapshot = models.PositiveIntegerField(null=True, blank=True, verbose_name="Количество зарегистрированных в квартире")

    class Meta:
        db_table = "OtherPayments"
        verbose_name = "Другие платежи"
        verbose_name_plural = "Другие платежи"
        ordering = ("id",)   

    def __str__(self):
        return f"OtherPayments {self.apartment.apartment_name}"


from django import forms

from services.models import ElectricityIndicators, GasIndicators, HotWaterIndicators, OtherPayments, WaterIndicators



# эта функция добавляет атрибут placeholder ва все поля, во всех классах форм, 
# а также устаналивает атрибут value для полей с малоизменяемыми данными во времени
def placeholder_last_entry(fields, last_entry):
    if last_entry:
        for field in fields:
            value = getattr(last_entry, field, None)

            if ("tariff" in field or "water_abon_plata" in field or 
            "electro_power_apartment" in field or "internet" in field or 
            "intercom" in field or "gas_delivery" in field):
                if value is not None:
                    fields[field].widget.attrs["value"] = value  # значение прямо в поле
                else:
                    fields[field].widget.attrs["placeholder"] = "Введите тариф"
            else:
                if value:
                    fields[field].widget.attrs["placeholder"] = f"Предыдущее значение: {value}"
                else:
                    fields[field].widget.attrs["placeholder"] = "Введите данные"
    else:
        for field in fields:
            fields[field].widget.attrs["placeholder"] = "Введите данные"


# class HasDataMixin создан для того, чтобы в незадействованные модели 
# (таблицы моделей) не вносились записи с нулевыми значениями [null]
class HasDataMixin:
    has_data = False  # флаг наличия непустых данных

    def clean(self):
        cleaned_data = super().clean()

        for field, value in cleaned_data.items():
            if value not in [None, '', 0]:
                self.has_data = True
                break

        return cleaned_data


class GasForm(HasDataMixin, forms.ModelForm):
    class Meta:
        model = GasIndicators
        # fields = '__all__'
        fields = [
            "gas_meter",
            "gas_tariff_counter",
            "gas_tariff_no_counter",
            "gas_delivery",
        ]

   
    
    def __init__(self, *args, apartment=None, last_entry=None, **kwargs, ):
        super().__init__(*args, **kwargs)

        self.apartment = apartment  # сохраняем объект
        # Сделаем поле не обязательным
        if apartment:
            if  apartment.has_gas is None:
                for field in self.fields.values():
                    field.required = False
            if apartment.has_gas == 0:
                self.fields["gas_meter"].required = False
                self.fields["gas_tariff_counter"].required = False
            elif apartment.has_gas == 1:
                self.fields["gas_tariff_no_counter"].required = False
            if not apartment.has_gas_delivery:
                self.fields["gas_delivery"].required = False
        print("last_entry")
        placeholder_last_entry(self.fields, last_entry)
       
class WaterForm(HasDataMixin, forms.ModelForm):
    class Meta:
        model = WaterIndicators
        fields = [
            "water_meter_one",
            "water_meter_two",
            "water_tariff_counter",
            "water_tariff_nocounter",
            "water_abon_plata",
        ]

    def __init__(self, *args, apartment=None, last_entry=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.apartment = apartment  # сохраняем объект
        # Сделаем поле не обязательным
        if apartment:
            if apartment.has_water is None:
                for field in self.fields.values():
                    field.required = False
            elif apartment.has_water == 0:
                self.fields["water_meter_one"].required = False
                self.fields["water_meter_two"].required = False
                self.fields["water_tariff_counter"].required = False

            elif apartment.has_water == 1:
                self.fields["water_meter_two"].required = False
                self.fields["water_tariff_nocounter"].required = False

            elif apartment.has_water == 2:
                self.fields["water_tariff_nocounter"].required = False

            if not apartment.has_water_abon_plata:
                self.fields["water_abon_plata"].required = False
        
           
        placeholder_last_entry(self.fields, last_entry)

class HotWaterForm(HasDataMixin, forms.ModelForm):
    class Meta:
        model = HotWaterIndicators
        fields = [
            "hot_water_meter",
            "hot_water_tariff_no_counter",
            "hot_water_tariff_counter",
            "heating_tariff_counter",
            "heating_tariff_no_counter",
        ]

    def __init__(self, *args, apartment=None, last_entry=None, **kwargs, ):
        super().__init__(*args, **kwargs)

        self.apartment = apartment  # сохраняем объект
        # Сделаем поле не обязательным
        if apartment:
            if apartment.has_hot_water is None:
                for field in self.fields.values():
                    field.required = False
            if apartment.has_hot_water == 0:
                self.fields["hot_water_meter"].required = False
                self.fields["heating_tariff_counter"].required = False
                self.fields["hot_water_tariff_counter"].required = False
            elif apartment.has_hot_water == 1:
                self.fields["heating_tariff_no_counter"].required = False
                self.fields["hot_water_tariff_no_counter"].required = False

        placeholder_last_entry(self.fields, last_entry)


class ElectricityForm(HasDataMixin, forms.ModelForm):
    class Meta:
        model = ElectricityIndicators
        fields = [
            "electro_meter_one",
            "electro_tariff_one",
            "electro_meter_two",
            "electro_tariff_two",
            "electro_power_apartment",
            "electro_tariff_no_counter",
        ]

    def __init__(self, *args, apartment=None, last_entry=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.apartment = apartment  # сохраняем объект
        # Сделаем поле не обязательным
        if apartment:
            if apartment.has_electricity is None:
                for field in self.fields.values():
                    field.required = False

            elif apartment.has_electricity == 0:
                self.fields["electro_meter_one"].required = False
                self.fields["electro_tariff_one"].required = False
                self.fields["electro_meter_two"].required = False
                self.fields["electro_tariff_two"].required = False

            elif apartment.has_electricity == 1:
                self.fields["electro_meter_two"].required = False
                self.fields["electro_tariff_two"].required = False
                self.fields["electro_power_apartment"].required = False
                self.fields["electro_tariff_no_counter"].required = False

            elif apartment.has_electricity == 2:
                self.fields["electro_power_apartment"].required = False
                self.fields["electro_tariff_no_counter"].required = False

        placeholder_last_entry(self.fields, last_entry)


class OtherForm(HasDataMixin, forms.ModelForm):
    class Meta:
        model = OtherPayments
        fields = [
            "tariff_apart_payment",
            "tariff_garbage",
            "tariff_lift",
            "tariff_heating",
            "internet",
            "intercom",
        ]

    def __init__(self, *args, apartment=None, last_entry=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.apartment = apartment

        if apartment:
            if not apartment.has_apart_payment:
                self.fields["tariff_apart_payment"].required = False
            if not apartment.has_garbage:
                self.fields["tariff_garbage"].required = False
            if not apartment.uses_lift:
                self.fields["tariff_lift"].required = False
            if not apartment.has_heating:
                self.fields["tariff_heating"].required = False
            if not apartment.has_internet:
                self.fields["internet"].required = False
            if not apartment.has_intercom:
                self.fields["intercom"].required = False

        placeholder_last_entry(self.fields, last_entry)

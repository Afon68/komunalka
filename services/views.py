from decimal import Decimal
import re
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from apartaments.models import Apartment
from services.table_el_other_all import electricity_table, other_table
from services.tables_gas_wat_hwat import gas_table, hot_water_table, water_table
from services.models import ElectricityIndicators, GasIndicators, HotWaterIndicators, OtherPayments, WaterIndicators
from services.forms import ElectricityForm, GasForm, HotWaterForm, OtherForm, WaterForm


# def indications(request, apartment_id):   # такие функции в джанго называются 'представление' или 'контроллер'
# apartment = get_object_or_404(Apartment, id=apartment_id, user=request.user)

# context = {
#     "apartment": apartment,
#     "title": "Внесение показаний",
#     "apartment_id": apartment_id,
# }
# return render(request, 'services/indications.html', context)


def indications_view(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    last_gas = GasIndicators.objects.filter(apartment=apartment).order_by("-timestamp").first()
    last_water = WaterIndicators.objects.filter(apartment=apartment).order_by("-timestamp").first()
    last_hot_water = HotWaterIndicators.objects.filter(apartment=apartment).order_by("-timestamp").first()
    last_electricity = ElectricityIndicators.objects.filter(apartment=apartment).order_by("-timestamp").first()
    last_other = OtherPayments.objects.filter(apartment=apartment).order_by("-timestamp").first()

    if request.method == "POST":
        gas_form = GasForm(request.POST, last_entry=last_gas, apartment=apartment)
        water_form = WaterForm(request.POST, last_entry=last_water, apartment=apartment)
        hot_water_form = HotWaterForm(request.POST, last_entry=last_hot_water, apartment=apartment)
        electricity_form = ElectricityForm(request.POST, last_entry=last_electricity, apartment=apartment)
        other_form = OtherForm(request.POST,last_entry=last_other, apartment=apartment)

        forms_valid = all([
            gas_form.is_valid(),
            water_form.is_valid(),
            hot_water_form.is_valid(),
            electricity_form.is_valid(),
            other_form.is_valid(),
        ])
        print("indications GasForm errors:", gas_form.errors)
        print("indications WaterForm errors:", water_form.errors)
        print("indications HotWaterForm errors:", hot_water_form.errors)
        print("indications ElectricityForm errors:", electricity_form.errors)
        print("indications OtherForm errors:", other_form.errors)
        print(f"forms_valid: {forms_valid}")


        if forms_valid:

            # Привязка квартиры к каждой форме и сохранение
            gas = gas_form.save(commit=False)
            gas.apartment = apartment
            gas.number_registered_snapshot = apartment.number_registered
            if gas_form.has_data:
                gas.save()

            water = water_form.save(commit=False)
            water.apartment = apartment
            water.number_registered_snapshot = apartment.number_registered
            if  water_form.has_data:
                water.save()

            hot_water = hot_water_form.save(commit=False)
            hot_water.apartment = apartment
            hot_water.number_registered_snapshot = apartment.number_registered
            if hot_water_form.has_data:
                hot_water.save()

            electricity = electricity_form.save(commit=False)
            electricity.apartment = apartment
            electricity.number_registered_snapshot = apartment.number_registered
            if electricity_form.has_data:
                electricity.save()

            other = other_form.save(commit=False)
            other.number_registered_snapshot = apartment.number_registered
            other.apartment = apartment
            if other_form.has_data:
                other.save()

            messages.success(request, "Показания успешно сохранены.")
            return redirect("services:tables", apartment_id=apartment_id)

        else:
            print("Проверьте корректность введённых данных.")
            messages.error(request, "Проверьте корректность введённых данных.")

    else:
        gas_form = GasForm(request.POST, last_entry=last_gas, apartment=apartment)
        water_form = WaterForm(request.POST, last_entry=last_water, apartment=apartment)
        hot_water_form = HotWaterForm(request.POST, last_entry=last_hot_water, apartment=apartment)
        electricity_form = ElectricityForm(request.POST, last_entry=last_electricity, apartment=apartment)
        other_form = OtherForm(request.POST,last_entry=last_other, apartment=apartment)

    context = {
        "last_gas": last_gas,
        "last_water": last_water,
        "last_hot_water": last_hot_water,
        "last_electricity": last_electricity,
        "last_other": last_other,
        "gas_form": gas_form,
        "water_form": water_form,
        "hot_water_form": hot_water_form,
        "electricity_form": electricity_form,
        "other_form": other_form,
        "apartment": apartment,
        "title": "Внесение показаний",
        "apartment_id": apartment_id,
    }

    return render(request,"services/indications_form.html", context)


def profile_last_entry(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    last_gas = GasIndicators.objects.filter(apartment=apartment).order_by("-timestamp").first()
    last_water = WaterIndicators.objects.filter(apartment=apartment).order_by("-timestamp").first()
    last_hot_water = HotWaterIndicators.objects.filter(apartment=apartment).order_by("-timestamp").first()
    last_electricity = ElectricityIndicators.objects.filter(apartment=apartment).order_by("-timestamp").first()
    last_other = OtherPayments.objects.filter(apartment=apartment).order_by("-timestamp").first()

    if request.method == "POST":
        # передаем apartment=apartment в каждую форму для определения обязательных  или необязательных полей,
        # без этого валидация не будет работать - будут ошибки,так как по умолчанию все поля обязательные
        gas_form = GasForm(request.POST, instance=last_gas, apartment=apartment)
        water_form = WaterForm(request.POST, instance=last_water, apartment=apartment)
        hot_water_form = HotWaterForm(request.POST, instance=last_hot_water, apartment=apartment)
        electricity_form = ElectricityForm(request.POST, instance=last_electricity, apartment=apartment)
        other_form = OtherForm(request.POST,instance=last_other, apartment=apartment)

        forms_valid = all([
            gas_form.is_valid(),
            water_form.is_valid(), 
            hot_water_form.is_valid(),
            electricity_form.is_valid(),
            other_form.is_valid(),
        ])



        print("profile GasForm errors:", gas_form.errors)
        print("profile WaterForm errors:", water_form.errors)
        print("profile HotWaterForm errors:", hot_water_form.errors)
        print("profile ElectricityForm errors:", electricity_form.errors)
        print("profile OtherForm errors:", other_form.errors)
        print(f"forms_valid: {forms_valid}")

        if forms_valid:
            gas = gas_form.save(commit=False)
            gas.apartment = apartment
            gas.number_registered_snapshot = apartment.number_registered
            if gas_form.has_data:
                gas.save()

            water = water_form.save(commit=False)
            water.apartment = apartment
            water.number_registered_snapshot = apartment.number_registered
            if  water_form.has_data:
                water.save()

            hot_water = hot_water_form.save(commit=False)
            hot_water.apartment = apartment
            hot_water.number_registered_snapshot = apartment.number_registered
            if hot_water_form.has_data:
                hot_water.save()

            electricity = electricity_form.save(commit=False)
            electricity.apartment = apartment
            electricity.number_registered_snapshot = apartment.number_registered
            if electricity_form.has_data:
                electricity.save()

            other = other_form.save(commit=False)
            other.number_registered_snapshot = apartment.number_registered
            other.apartment = apartment
            if other_form.has_data:
                other.save()


            print("Показания успешно сохранены.")
            messages.success(request, "Показания успешно сохранены.")
            return redirect("services:tables", apartment_id=apartment.id)

        else:
            print("Проверьте корректность введённых данных.")
            messages.error(request, "last entry:Проверьте корректность введённых данных.")

    else:
        gas_form = GasForm(instance=last_gas)
        water_form = WaterForm(instance=last_water)
        hot_water_form = HotWaterForm(instance=last_hot_water)
        electricity_form = ElectricityForm(instance=last_electricity)
        other_form = OtherForm(instance=last_other)

    context = {
        "last_gas": last_gas,
        "gas_form": gas_form,
        "water_form": water_form,
        "hot_water_form": hot_water_form,
        "electricity_form": electricity_form,
        "other_form": other_form,
        "apartment": apartment,
        "title": "Редактировать последние показания",
        "apartment_id": apartment_id,
    }

    return render(request, "services/profile_last_entry.html", context)

def tables(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id, user=request.user)

    gas = GasIndicators.objects.filter(apartment=apartment).order_by("-timestamp")
    water = WaterIndicators.objects.filter(apartment=apartment).order_by("-timestamp")
    hot_water = HotWaterIndicators.objects.filter(apartment=apartment).order_by("-timestamp")
    electricity = ElectricityIndicators.objects.filter(apartment=apartment).order_by("-timestamp")
    other = OtherPayments.objects.filter(apartment=apartment).order_by("-timestamp")

    gas_data = gas_table(request, gas, apartment)
    water_data = water_table(request, water, apartment)
    hot_water_data = hot_water_table(request, hot_water, apartment)
    electricity_data = electricity_table(request, electricity, apartment)
    other_data = other_table(request, other, apartment)
    #  функция  получения списка услуг для шаблона "services/tables.html"
    services = apartaments_services(request, apartment_id)
    first_tab = None
    tabs = table_tabs(request, apartment_id)
    if tabs:
        first_tab = tabs[0][1]

    payments = [gas_data, water_data, hot_water_data, electricity_data, other_data]
    summary = all_payments(request, apartment, gas_data, water_data, hot_water_data, electricity_data, other_data)

    warn = all([len(gas_data) < 2, len(water_data) < 2, len(hot_water_data) < 2, len(electricity_data) < 2, len(other_data) < 2,]) 

    context = {
        "apartment": apartment,
        "gas_data": gas_data,
        "water_data": water_data,
        "hot_water_data": hot_water_data,
        "electricity_data": electricity_data,
        "other_data": other_data,
        "title": "Таблицы расходов",
        "services": services,
        "tabs": tabs,
        "first_tab": first_tab,
        "payments": payments,
        "summary": summary,
        "warn": warn,
        "apartment_id": apartment_id if apartment else None,

    }
    return render(request, "services/tables.html", context) 

#  функция  получения списка услуг для шаблона "services/tables.html"
def apartaments_services(request, apartment_id):
    if request.user and apartment_id:
        apartment = get_object_or_404(Apartment, id=apartment_id, user=request.user) #get_object_or_404(Apartment, id=apartment_id, user=request.user)
        list_verbose_name = []
        for field in apartment._meta.fields:
            if field.verbose_name in [
                "Газ",
                "Электричество",
                "Лифт",
                "Доставка газа",
                "Вывоз мусора",
                "Квартплата",
                "Интернет",
                "Домофон",
                "Центральное отопление",
            ]:
                
                value = getattr(apartment, field.name)
                if value is True or (isinstance(value, int) and not isinstance(value, bool) and value >= 0):
                    list_verbose_name.append(field.verbose_name)
             
        return list_verbose_name
    
    
def table_tabs(request, apartment_id):
    if request.user and apartment_id:
        apartment = get_object_or_404(Apartment, id=apartment_id, user=request.user) #get_object_or_404(Apartment, id=apartment_id, user=request.user)
        list_table_tabs = []
        
        for tab in [
                ["Газ","gas"],
               ["Вода","water"],
               ["Горячая вода","hot_water"],
               ["Электричество","electricity"],
               ["Остальные услуги","other"],
            ]:
               
            if tab == ["Газ","gas"]:
                if apartment.has_gas is not None:
                    list_table_tabs.append(tab)    
            if tab == ["Вода","water"]:
                if apartment.has_water is not None:
                    list_table_tabs.append(tab)    
            if tab == ["Горячая вода","hot_water"]:
                if apartment.has_hot_water is not None:
                    list_table_tabs.append(tab)    
            if tab == ["Электричество","electricity"]:
                if apartment.has_electricity is not None:
                    list_table_tabs.append(tab)    
            if tab == ["Остальные услуги","other"]:
                if (apartment.uses_lift or apartment.has_garbage or 
                apartment.has_apart_payment or apartment.has_internet or 
                apartment.has_intercom or apartment.has_heating):
                    list_table_tabs.append(tab)    
            
        return list_table_tabs
    
def all_payments(request, payments):
    total = 0
    pays = []
    
    # for payment_group in payments:
    #     for item in payment_group:
def all_payments(request, apartment, gas_data, water_data, hot_water_data, electricity_data, other_data):
    total_amount = 0
   # Пример объединения данных по индексу
    summary = []
    for i in range(max(len(gas_data), len(water_data), len(hot_water_data), len(electricity_data), len(other_data))):
        row = {}
        
        row['timestamp'] = gas_data[i]["timestamp"] if i < len(gas_data) else None
        row['gas_total'] = gas_data[i]["gas_total"] if i < len(gas_data) else None
        row['gas_delivery'] = gas_data[i]["gas_delivery"] if i < len(gas_data) else None
        row['el_total'] = electricity_data[i]["el_total"] if i < len(electricity_data) else None
        row['total_lift'] = other_data[i]["total_lift"] if i < len(other_data) else None
        row['total_garbage'] = other_data[i]["total_garbage"] if i < len(other_data) else None
        row['total_apart_payment'] = other_data[i]["total_apart_payment"] if i < len(other_data) else None
        row['internet'] = other_data[i]["internet"] if i < len(other_data) else None
        row['intercom'] = other_data[i]["intercom"] if i < len(other_data) else None
        row['general_heating'] = other_data[i]["total_heating"] if i < len(other_data) else None
        if not apartment.has_water_abon_plata:
            row['water_total'] = water_data[i]["water_total"] if i < len(water_data) else None
        else:
            row['total_with_abon_plata'] = water_data[i]["total_with_abon_plata"] if i < len(water_data) else None
        row['total_heating'] = hot_water_data[i]["total_heating"] if i < len(hot_water_data) else None
        row['total_water'] =hot_water_data[i]["total_water"] if i < len(hot_water_data) else None
        
        
        summary.append(row)
        
    for i in range(len(summary)): #summary:
        total_amount = Decimal(0.00)
        if i == len(summary) - 1:
            total_amount = Decimal(0.00)
        else:
            for key in summary[i]:
                if key == "timestamp":
                    continue
                if summary[i][key] is not None:
                    total_amount += Decimal(summary[i][key])
                    print(key,summary[i][key])
        print(f"total_amount={total_amount}")           
        summary[i]['total_amount'] = total_amount
   
    return summary
    
                    

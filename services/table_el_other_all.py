from calendar import c
from math import e
from tkinter import N
from tkinter.messagebox import NO

from django.contrib import messages


def electricity_table(request, electricity, apartment):
   
    if apartment.has_electricity is not None:
        electricity_data = []
        for i in range(len(electricity)):
            # if apartment.has_gas == 1:
            if i < len(electricity) - 1:
                # counter#1
                current_value_one = electricity[i].electro_meter_one  # current_
                prev_value_one = electricity[i + 1].electro_meter_one

                if prev_value_one and current_value_one:
                    consumption_one = current_value_one - prev_value_one
                elif not prev_value_one and current_value_one:
                    consumption_one = 0
                else:
                    consumption_one = None

                # counter#2
                current_value_two = electricity[i].electro_meter_two  # current_
                prev_value_two = electricity[i + 1].electro_meter_two

                if prev_value_two and current_value_two:
                    consumption_two = current_value_two - prev_value_two
                elif not prev_value_two and current_value_two :
                    consumption_two = 0
                else:
                    consumption_two = None

            #  обработка последнего или единственного элемента
            elif i == len(electricity) - 1:
                prev_value_one = 0
                consumption_one = 0
                prev_value_two = 0
                consumption_two = 0

            total = None
            if apartment.has_electricity == 0:
                if (electricity[i].electro_tariff_no_counter and electricity[i].electro_power_apartment):
                    total = round(electricity[i].electro_tariff_no_counter * electricity[i].electro_power_apartment,2)
                else:
                    total = 0
                    messages.error(request, "Электро!!!Проверьте корректность введённых данных.")
            elif apartment.has_electricity == 1:
                if (consumption_one is not None and consumption_one >= 0 and electricity[i].electro_tariff_one ):
                    total = round(consumption_one * electricity[i].electro_tariff_one, 2)
                else:
                    total = 0
                    messages.error(request, "Электро!!!Проверьте корректность введённых данных.")
            elif apartment.has_electricity == 2:
                total_one = None
                total_two = None
                if (consumption_one is not None and consumption_one >= 0 and electricity[i].electro_tariff_one):
                    total_one = consumption_one * electricity[i].electro_tariff_one

                if (consumption_two is not None and consumption_two >= 0 and electricity[i].electro_tariff_two):
                    total_two = consumption_two * electricity[i].electro_tariff_two
                    
                if total_one is not None and total_two is not None:
                    total = round(total_one + total_two, 2)

                else:
                    messages.error(request, "Электро!!!Проверьте корректность введённых данных.")

            electricity_data.append(
                {
                    "timestamp": electricity[i].timestamp,
                    "prev_value_one": prev_value_one,
                    "electro_meter_one": electricity[i].electro_meter_one,
                    "consumption_one": consumption_one,
                    "prev_value_two": prev_value_two,
                    "electro_meter_two": electricity[i].electro_meter_two,
                    "consumption_two": consumption_two,
                    "electro_tariff_one": electricity[i].electro_tariff_one, 
                    "electro_tariff_two": electricity[i].electro_tariff_two,
                    "electro_tariff_no_counter": electricity[i].electro_tariff_no_counter,
                    "electro_power_apartment": electricity[i].electro_power_apartment,
                    "el_total": total,
                    
                }   
            )
        # print(f"electricity_data: {electricity_data}")  # Добавляем вывод water_data)    
    else:
        # messages.error(request, "Не указано, подключена ли вода к квартире.")
        return []
  
    return electricity_data

def other_table(request, other, apartment):
    other_data = []
    for i in range(len(other)):
        current = other[i]
        total_apart_payment = None
        total_garbage = None
        total_heating = None
        total_lift = None
        internet = None
        intercom = None

        if apartment.has_apart_payment:
            if current.tariff_apart_payment and current.number_registered_snapshot:
                total_apart_payment = current.tariff_apart_payment * current.number_registered_snapshot

        if apartment.has_garbage:
            if current.tariff_garbage and current.number_registered_snapshot:
                total_garbage = current.tariff_garbage * current.number_registered_snapshot

        if apartment.uses_lift:
            if current.tariff_lift and current.number_registered_snapshot:
                total_lift = current.tariff_lift * current.number_registered_snapshot

        if apartment.has_heating:
            if current.tariff_heating  and apartment.area_apartment is not None:
                total_heating = current.tariff_heating * apartment.area_apartment

        if apartment.has_internet:
            if current.internet:
                internet = current.internet

        if apartment.has_intercom:
            if current.intercom:
                intercom = current.intercom

        other_data.append(
            {
                "timestamp": current.timestamp,
                "number_registered_snapshot": current.number_registered_snapshot,
                "tariff_apart_payment": current.tariff_apart_payment,
                "total_apart_payment": total_apart_payment,
                "tariff_garbage": current.tariff_garbage,
                "total_garbage": total_garbage,
                "tariff_heating": current.tariff_heating,
                "total_heating": total_heating,
                "tariff_lift": current.tariff_lift,
                "total_lift": total_lift,
                "area_apartment": apartment.area_apartment,
                "internet": internet,
                "intercom": intercom,
            }
        )
    return other_data
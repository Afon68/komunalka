from calendar import c
from math import e
from django.contrib import messages


def gas_table(request, gas, apartment):
    
    gas_data = []
    for i in range(len(gas)):
        # if apartment.has_gas == 1:
        if i < len(gas) - 1:
            prev_value = gas[i + 1].gas_meter
            if prev_value and gas[i].gas_meter:
                consumption = gas[i].gas_meter - prev_value
            elif gas[i].gas_meter and not prev_value:
                consumption = 0
            else:
                consumption = None
        elif i == len(gas) - 1:
            prev_value = 0
            consumption = 0
        total = None
        if apartment.has_gas == 0:
            if gas[i].gas_tariff_no_counter and gas[i].number_registered_snapshot:
                total = round(
                    gas[i].gas_tariff_no_counter * gas[i].number_registered_snapshot, 2
                )
            else:
                # total = None
                messages.error(
                    request, "Газ!!! Проверьте корректность введённых данных."
                )
        else:
            if (
                consumption is not None
                and consumption >= 0
                and gas[i].gas_tariff_counter
            ):
                total = round(consumption * gas[i].gas_tariff_counter, 2)
            else:
                messages.error(
                    request, "Газ!!! Проверьте корректность введённых данных."
                )

        gas_data.append(
            {
                "timestamp": gas[i].timestamp,
                "prev_value": prev_value,
                "gas_meter": gas[i].gas_meter,
                "consumption": consumption,
                "gas_tariff_counter": gas[i].gas_tariff_counter,
                "gas_tariff_no_counter": gas[i].gas_tariff_no_counter,
                "number_registered": gas[i].number_registered_snapshot,
                "gas_total": total,
                "gas_delivery": gas[i].gas_delivery,
            }
        )
    # print(f"gas_data: {gas_data}")  # print(gas_data)    
    return gas_data


def water_table(request, water, apartment):
    if apartment.has_water is not None:
        water_data = []
        for i in range(len(water)):
            # if apartment.has_gas == 1:
            if i < len(water) - 1:
                # counter#1
                current_value_one = water[i].water_meter_one  # current_
                prev_value_one = water[i + 1].water_meter_one

                if prev_value_one and current_value_one:
                    consumption_one = current_value_one - prev_value_one
                elif current_value_one and not prev_value_one:
                    consumption_one = 0
                else:
                    consumption_one = None

                # counter#2
                current_value_two = water[i].water_meter_two  # current_
                prev_value_two = water[i + 1].water_meter_two

                if prev_value_two and current_value_two:
                    consumption_two = current_value_two - prev_value_two
                elif water[i].water_meter_two and not prev_value_two:
                    consumption_two = 0
                else:
                    consumption_two = None

            #  обработка последнего или единственного элемента
            elif i == len(water) - 1:
                prev_value_one = 0
                consumption_one = 0
                prev_value_two = 0
                consumption_two = 0

            total = None
            if apartment.has_water == 0:
                if (water[i].water_tariff_nocounter and water[i].number_registered_snapshot):
                    total = round(water[i].water_tariff_nocounter * water[i].number_registered_snapshot,2)
                else:
                    messages.error(request, "Вода!!!Проверьте корректность введённых данных.")
            elif apartment.has_water == 1:
                if (consumption_one is not None and consumption_one >= 0 and water[i].water_tariff_counter):
                    total = round(consumption_one * water[i].water_tariff_counter, 2)
                else:
                    messages.error(request, "Вода!!!Проверьте корректность введённых данных.")
            elif apartment.has_water == 2:
                total_one = None
                total_two = None
                if (consumption_one is not None and consumption_one >= 0 and water[i].water_tariff_counter):
                    total_one = consumption_one * water[i].water_tariff_counter

                if (consumption_two is not None and consumption_two >= 0 and water[i].water_tariff_counter):
                    total_two = consumption_two * water[i].water_tariff_counter

                if total_one is not None and total_two is not None:
                    total = round(total_one + total_two, 2)

                else:
                    messages.error(request, "Вода!!!Проверьте корректность введённых данных.")

            total_with_abon_plata = 0.00
            if total and water[i].water_abon_plata:
                total_with_abon_plata = round(total + water[i].water_abon_plata, 2)

            water_data.append(
                {
                    "timestamp": water[i].timestamp,
                    "prev_value_one": prev_value_one,
                    "water_meter_one": water[i].water_meter_one,
                    "consumption_one": consumption_one,
                    "prev_value_two": prev_value_two,
                    "water_meter_two": water[i].water_meter_two,
                    "consumption_two": consumption_two,
                    "water_tariff_counter": water[i].water_tariff_counter,
                    "water_tariff_nocounter": water[i].water_tariff_nocounter,
                    "number_registered_snapshot": water[i].number_registered_snapshot,
                    "water_total": total,
                    "water_abon_plata": water[i].water_abon_plata,
                    "total_with_abon_plata": total_with_abon_plata,
                }
            )
        # print(f"water_data: {water_data}")  # Добавляем вывод water_data)    
    else:
        # messages.error(request, "Не указано, подключена ли вода к квартире.")
        return []
    return water_data


def hot_water_table(request, hot_water, apartment):
    if apartment.has_hot_water is None:
        # messages.error(request, "Не указано, подключена ли вода к квартире.")
        return []

    hot_water_data = []
    for i in range(len(hot_water)):
        current = hot_water[i]
        prev_entry = hot_water[i + 1] if i < len(hot_water) - 1 else None

        # Значения по умолчанию
        prev_value = 0
        consumption = 0
        total_water = 0
        total_heating = 0
        # Считаем расход
        if prev_entry:
            prev_value = prev_entry.hot_water_meter
            if current.hot_water_meter is not None and prev_value is not None:
                consumption = current.hot_water_meter - prev_value

            elif current.hot_water_meter is not None and not prev_value :
                consumption = 0

            else:
                # если единстевенная или последняя запись в таблице
                consumption = 0
        else:
            # если единстевенная или последняя запись в таблице
            consumption = 0

        # Расчёт total
        if apartment.has_hot_water == 0:
            # Без счётчика
            if current.hot_water_tariff_no_counter is not None and current.number_registered_snapshot is not None:
                total_water = round(current.hot_water_tariff_no_counter * current.number_registered_snapshot,2)
            if current.heating_tariff_no_counter is not None and current.number_registered_snapshot is not None:
                total_heating = round(current.heating_tariff_no_counter * current.number_registered_snapshot,2)
            else:
                messages.error(request,f"Горячая вода!!!Недостаточно данных для расчёта без счётчика за {current.timestamp}.")
            # print(f"water[i].water_tariff_nocounter: {water[i].water_tariff_nocounter}")    
        elif apartment.has_hot_water == 1:
            # со счётчиком
            if consumption is not None and consumption >= 0 and current.hot_water_tariff_counter:
                total_water = round(consumption * current.hot_water_tariff_counter, 2)
            if consumption is not None and consumption >= 0 and current.heating_tariff_counter:   
                total_heating = round(consumption * current.heating_tariff_counter, 2)
            else:
                messages.error(request,f"Горячая вода!!!Ошибка в расчётах с одним счётчиком за {current.timestamp}.")
        
        hot_water_data.append(
            {
                "timestamp": current.timestamp,
                "hot_prev_value": prev_value,
                "hot_water_meter": current.hot_water_meter,
                "hot_consumption": consumption,
                "hot_water_tariff_counter": current.hot_water_tariff_counter,
                "hot_water_tariff_no_counter": current.hot_water_tariff_no_counter,
                "heating_tariff_no_counter": current.heating_tariff_no_counter,
                "heating_tariff_counter": current.heating_tariff_counter,
                "number_registered": current.number_registered_snapshot,
                "total_water": total_water,
                "total_heating": total_heating,
            }
        )
                
    return hot_water_data



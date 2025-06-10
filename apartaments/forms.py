from django import forms
from .models import Apartment


class ApartmentForm(forms.ModelForm):
    # Чекбоксы и радиокнопки нужно переопределить, чтобы контролировать их вид и значение
    has_gas_checkbox = forms.BooleanField(required=False, label="Газ.")
    gas_type = forms.ChoiceField(
        choices=[("0", "Без счётчика"), ("1", "1 счётчик")],
        widget=forms.RadioSelect,
        required=False,
        label="Количество счётчиков",
        initial=1,
    )

    has_water_checkbox = forms.BooleanField(required=False, label="Вода.")
    water_type = forms.ChoiceField(
        choices=[("0", "Без счётчика"), ("1", "1 счётчик"), ("2", "2 счётчика")],
        widget=forms.RadioSelect,
        required=False,
        label="Количество счётчиков",
        initial=1,
    )
    has_hot_water_checkbox = forms.BooleanField(required=False, label="Горячая вода.")
    hot_water_type = forms.ChoiceField(
        choices=[("0", "Без счётчика"), ("1", "1 счётчик")],
        widget=forms.RadioSelect,
        required=False,
        label="Количество счётчиков",
        initial=1,
    )

    has_electricity_checkbox = forms.BooleanField(required=False, label="Электричество.")
    elektrika_type = forms.ChoiceField(
        choices=[("0", "Без счётчика"), ("1", "Счётчик 1"), ("2", "Счётчик 2")],
        widget=forms.RadioSelect,
        required=False,
        label="Количество счётчиков",
        initial=1,
    )

    

    # init переопределяется для того, чтобы при редактировании профайла квартиры
    # не падали флаги чекбоксов и радиокнопок
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            # Газ
            self.fields["has_gas_checkbox"].initial = instance.has_gas is not None
            self.fields["gas_type"].initial = str(instance.has_gas) if instance.has_gas is not None else "1"

            # Вода
            self.fields["has_water_checkbox"].initial = instance.has_water is not None
            self.fields["water_type"].initial = str(instance.has_water) if instance.has_water is not None else "1"

            # Горячая вода
            self.fields["has_hot_water_checkbox"].initial = instance.has_hot_water is not None
            self.fields["hot_water_type"].initial = str(instance.has_hot_water) if instance.has_hot_water is not None else "1"

            # Электричество
            self.fields["has_electricity_checkbox"].initial = instance.has_electricity is not None
            self.fields["elektrika_type"].initial = str(instance.has_electricity) if instance.has_electricity is not None else "1"

    class Meta:
        model = Apartment
        fields = [
            "apartment_name",
            "uses_lift",
            "has_garbage",
            "has_apart_payment",
            "has_internet",
            "has_intercom",
            "has_heating",
            "area_apartment",
            "number_registered",
            "has_gas_delivery",
            "has_water_abon_plata",
        ]

    # Функция, которая проверяет уникальность названий квартир
    def clean_apartment_name(self):
        name = self.cleaned_data["apartment_name"]

        # Исключаем текущий объект при редактировании квартиры
        qs = Apartment.objects.filter(apartment_name=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Квартира с таким названием уже существует.")

        return name

    # self.instance — это объект Apartment, связанный с этой формой (либо новый, либо редактируемый).

    # self.instance.pk — это его первичный ключ (id). Он есть только у существующего объекта, который редактируется.

    # ✅ Если self.instance.pk есть — это значит, форма используется для редактирования.

    # Тогда qs.exclude(pk=self.instance.pk) исключает текущую редактируемую квартиру из поиска дубликатов.

    def clean(self):
        cleaned_data = super().clean()

        has_heating = cleaned_data.get("has_heating")
        area_apartment = cleaned_data.get("area_apartment")
        number_registered = cleaned_data.get("number_registered")
        uses_lift = cleaned_data.get("uses_lift")
        has_garbage = cleaned_data.get("has_garbage")
        has_apart_payment = cleaned_data.get("has_apart_payment")

        if has_heating and not area_apartment:
            self.add_error(
                "area_apartment",
                "Укажите пожалуйста площадь квартиры при наличии отопления.",
            )

        # Присваиваем значение полям модели на основе чекбоксов и радиокнопок
        if cleaned_data.get("has_gas_checkbox"):
            cleaned_data["has_gas"] = int(cleaned_data.get("gas_type") or 0)
        else:
            cleaned_data["has_gas"] = None

        if cleaned_data.get("has_water_checkbox"):
            cleaned_data["has_water"] = int(cleaned_data.get("water_type") or 0)
        else:
            cleaned_data["has_water"] = None

        if cleaned_data.get("has_hot_water_checkbox"):
            cleaned_data["has_hot_water"] = int(cleaned_data.get("hot_water_type") or 0)
        else:
            cleaned_data["has_hot_water"] = None

        if cleaned_data.get("has_electricity_checkbox"):
            cleaned_data["has_electricity"] = int(
                cleaned_data.get("elektrika_type") or 0
            )
        else:
            cleaned_data["has_electricity"] = None

        if (uses_lift
            or has_garbage
            or has_apart_payment
            or cleaned_data["has_gas"] == 0
            or cleaned_data["has_water"] == 0
        ) and not number_registered:
            self.add_error("area_apartment", "Укажите пожалуйста количество зарегистрированных в квартире!!!")  

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        cleaned_data = self.cleaned_data
        instance.has_gas = cleaned_data.get("has_gas")
        instance.has_water = cleaned_data.get("has_water")
        instance.has_hot_water = cleaned_data.get("has_hot_water")
        instance.has_electricity = cleaned_data.get("has_electricity")

        if commit:
            instance.save()
        return instance






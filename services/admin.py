from django.contrib import admin

from services.models import ElectricityIndicators, GasIndicators, HotWaterIndicators, OtherPayments, WaterIndicators

admin.site.register(GasIndicators)
admin.site.register(WaterIndicators)
admin.site.register(HotWaterIndicators)
admin.site.register(ElectricityIndicators)
admin.site.register(OtherPayments)

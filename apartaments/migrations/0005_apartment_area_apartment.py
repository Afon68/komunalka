# Generated by Django 5.2 on 2025-05-21 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartaments', '0004_apartment_has_intercom_alter_otherpayments_intercom'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='area_apartment',
            field=models.PositiveIntegerField(null=True, verbose_name='Площадь квартиры.'),
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-28 18:51

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("rest", "0006_rename_otc_customuser_patronymic_and_more"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="customuser",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]

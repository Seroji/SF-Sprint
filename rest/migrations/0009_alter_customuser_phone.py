# Generated by Django 4.2.1 on 2023-05-28 19:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rest", "0008_customuser_date_joined_customuser_is_active_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="phone",
            field=models.BigIntegerField(default="9999999999"),
        ),
    ]

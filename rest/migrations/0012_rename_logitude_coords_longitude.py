# Generated by Django 4.2.1 on 2023-05-28 21:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("rest", "0011_alter_level_autumn_alter_level_spring_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="coords",
            old_name="logitude",
            new_name="longitude",
        ),
    ]

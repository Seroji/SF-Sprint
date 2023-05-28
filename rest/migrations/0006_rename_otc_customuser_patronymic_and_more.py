# Generated by Django 4.2.1 on 2023-05-28 18:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rest", "0005_customuser_otc"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customuser",
            old_name="otc",
            new_name="patronymic",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="user",
        ),
        migrations.AddField(
            model_name="customuser",
            name="email",
            field=models.EmailField(
                default="example@mail.ru", max_length=64, unique=True
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="first_name",
            field=models.CharField(default="Имя", max_length=64),
        ),
        migrations.AddField(
            model_name="customuser",
            name="is_superuser",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="customuser",
            name="last_login",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last login"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="last_name",
            field=models.CharField(default="Фамилия", max_length=64),
        ),
        migrations.AddField(
            model_name="customuser",
            name="password",
            field=models.CharField(default="password"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="username",
            field=models.CharField(default="username", max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="phone",
            field=models.IntegerField(default="9999999999"),
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-30 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0017_perevaladded_connect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='autumn',
            field=models.CharField(default='', max_length=2),
        ),
        migrations.AlterField(
            model_name='level',
            name='spring',
            field=models.CharField(default='', max_length=2),
        ),
        migrations.AlterField(
            model_name='level',
            name='summer',
            field=models.CharField(default='', max_length=2),
        ),
        migrations.AlterField(
            model_name='level',
            name='winter',
            field=models.CharField(default='', max_length=2),
        ),
    ]

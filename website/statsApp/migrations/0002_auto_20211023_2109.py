# Generated by Django 3.2.4 on 2021-10-23 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statsApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='avgra',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='team',
            name='avgrs',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=5),
        ),
    ]

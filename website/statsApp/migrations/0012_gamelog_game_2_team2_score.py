# Generated by Django 3.2.4 on 2021-10-30 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statsApp', '0011_auto_20211030_0240'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamelog',
            name='game_2_team2_score',
            field=models.IntegerField(default=0),
        ),
    ]

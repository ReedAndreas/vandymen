# Generated by Django 3.2.4 on 2021-10-30 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statsApp', '0008_gamelog_player1'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['team']},
        ),
        migrations.RemoveField(
            model_name='gamelog',
            name='player1',
        ),
    ]

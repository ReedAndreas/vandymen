# Generated by Django 3.2.4 on 2021-10-30 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statsApp', '0014_auto_20211030_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='average_run_scored',
            new_name='average_runs_scored',
        ),
    ]

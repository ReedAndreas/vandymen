# Generated by Django 3.2.4 on 2021-10-29 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('gp', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('gp', models.IntegerField(default=0)),
                ('ab', models.IntegerField(default=0)),
                ('h', models.IntegerField(default=0)),
                ('db', models.IntegerField(default=0)),
                ('tr', models.IntegerField(default=0)),
                ('hr', models.IntegerField(default=0)),
                ('rbi', models.IntegerField(default=0)),
                ('k', models.IntegerField(default=0)),
                ('bb', models.IntegerField(default=0)),
                ('ba', models.DecimalField(decimal_places=3, default=0.0, max_digits=4)),
                ('sp', models.DecimalField(decimal_places=3, default=0.0, max_digits=4)),
                ('obp', models.DecimalField(decimal_places=3, default=0.0, max_digits=4)),
                ('ops', models.DecimalField(decimal_places=3, default=0.0, max_digits=4)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='statsApp.team')),
            ],
        ),
    ]

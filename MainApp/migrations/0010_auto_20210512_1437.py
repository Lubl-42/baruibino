# Generated by Django 3.1 on 2021-05-12 14:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0009_auto_20210424_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='elektro',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MainApp.account'),
        ),
        migrations.AlterField(
            model_name='account',
            name='comment',
            field=models.CharField(default='Начисление без комментариев, автоматическое', max_length=500),
        ),
        migrations.AlterField(
            model_name='account',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 14, 37, 55, 303316)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 14, 37, 55, 302889)),
        ),
        migrations.AlterField(
            model_name='elektro',
            name='comment',
            field=models.CharField(default='No comment', max_length=500),
        ),
        migrations.AlterField(
            model_name='elektro',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 14, 37, 55, 303851)),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 14, 37, 55, 302282)),
        ),
        migrations.AlterField(
            model_name='tarif',
            name='comment',
            field=models.CharField(default='No comment', max_length=500),
        ),
        migrations.AlterField(
            model_name='tarif',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 14, 37, 55, 304227)),
        ),
    ]

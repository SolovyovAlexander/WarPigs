# Generated by Django 3.1.2 on 2020-10-14 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20201014_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raid',
            name='preparation_time',
            field=models.TimeField(blank=True, default='00:00:30', null=True, verbose_name='preparation time'),
        ),
    ]
# Generated by Django 3.1.2 on 2020-10-12 17:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_pig_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pig',
            name='upgrade_started',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='upgrade started'),
        ),
    ]

# Generated by Django 4.1.4 on 2023-03-05 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_product_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='size',
            name='label_shoes',
            field=models.CharField(blank=True, choices=[('rus', 'RUS'), ('uk', 'UK'), ('us', 'US'), ('eur', 'EUR'), ('sm', 'SM')], default='rus', max_length=3, null=True, verbose_name='Система размера обуви'),
        ),
        migrations.AlterField(
            model_name='size',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]

# Generated by Django 4.1.4 on 2023-01-02 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_remove_product_category_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='Старая цена'),
        ),
    ]

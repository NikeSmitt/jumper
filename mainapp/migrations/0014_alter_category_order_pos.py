# Generated by Django 4.1.4 on 2023-04-25 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='order_pos',
            field=models.PositiveSmallIntegerField(blank=True, null=True, unique=True, verbose_name='Позиция в хедере'),
        ),
    ]

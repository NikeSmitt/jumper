# Generated by Django 4.1.4 on 2023-02-11 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=10, verbose_name='Номер заказа')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Имя заказчика')),
                ('phone', models.CharField(max_length=12, verbose_name='Телефон заказчика для обратной связи')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email заказчика')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Имя заказчика')),
                ('address', models.CharField(blank=True, max_length=300, null=True, verbose_name='Адрес заказчика')),
                ('city', models.CharField(blank=True, max_length=30, null=True, verbose_name='Город заказчика')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('comment', models.CharField(blank=True, max_length=500, null=True, verbose_name='Дополнения к заказу')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='orderapp.order', verbose_name='К какому заказу относится')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.product', verbose_name='Товар в заказе')),
                ('size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.size', verbose_name='Размер товара')),
            ],
            options={
                'verbose_name': 'Продукт в заказе',
                'verbose_name_plural': 'Продукты в заказе',
            },
        ),
    ]

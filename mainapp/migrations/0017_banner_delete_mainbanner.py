# Generated by Django 4.1.4 on 2023-04-25 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('mainapp', '0016_rename_category_product_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(blank=True, default='banner', max_length=200, null=True)),
                ('subtitle', models.CharField(blank=True, max_length=200, null=True)),
                ('show', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='banners/')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['-title'],
            },
        ),
        migrations.DeleteModel(
            name='MainBanner',
        ),
    ]
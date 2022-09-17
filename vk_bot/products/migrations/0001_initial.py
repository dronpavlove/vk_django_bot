# Generated by Django 4.1.1 on 2022-09-17 12:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.BooleanField(default=True, help_text='Если категория активна, то она должна отображаться в главном меню сайта', verbose_name='активность')),
                ('icon_photo', models.FileField(max_length=500, upload_to='categories/', validators=[django.core.validators.FileExtensionValidator(['jpeg', 'jpg', 'png', 'svg'])], verbose_name='иконка категории')),
                ('category_name', models.CharField(max_length=1000, unique=True, verbose_name='название категории')),
                ('description', models.TextField(blank=True, help_text='Опишите, например, какие товары соответствуют данной категории', verbose_name='описание')),
            ],
            options={
                'verbose_name': 'категория каталога товаров',
                'verbose_name_plural': 'категории каталога товаров',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='название товара')),
                ('article', models.CharField(max_length=100, verbose_name='артикул')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='описание товара')),
                ('price', models.DecimalField(decimal_places=2, default=1, max_digits=12, validators=[django.core.validators.MinValueValidator(1)], verbose_name='цена')),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='рейтинг')),
                ('flag_limit', models.BooleanField(default=False, verbose_name='товар заканчивается')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', related_query_name='product', to='products.category', verbose_name='категория каталога')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True, verbose_name='имя свойства')),
                ('tooltip', models.CharField(blank=True, default='', help_text='Опишите подробнее, что это за свойство товара', max_length=1000, verbose_name='примечание')),
                ('alias', models.CharField(help_text='Псевдоним участвует в построении фильтра для свойства и должен соответствовать выражению ^[a-zA-Z][_a-zA-Z0-9]*$', max_length=300, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex=re.compile('^[a-zA-Z][_a-zA-Z0-9]*$'))], verbose_name='Псевдоним')),
            ],
            options={
                'verbose_name': 'свойство товара',
                'verbose_name_plural': 'свойства товаров',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='PropertyProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, default=None, max_length=1000, null=True, verbose_name='значение свойства')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_properties', related_query_name='product_property', to='products.product', verbose_name='товар')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_properties', related_query_name='product_property', to='products.property', verbose_name='свойство товара')),
            ],
            options={
                'verbose_name': 'параметр свойства товара',
                'verbose_name_plural': 'параметры свойства товара',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='PropertyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filtered', models.BooleanField(default=True, help_text='Если отмечено, то можно будет фильтровать товары по этому свойству', verbose_name='фильтр')),
                ('filter_position', models.PositiveIntegerField(default=1, help_text='Свойства в фильтре будут располагаться в порядке возрастания позиции', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Позиция в фильтре')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_properties', related_query_name='category_property', to='products.category', verbose_name='категория')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_properties', related_query_name='category_property', to='products.property', verbose_name='свойство товаров в категории')),
            ],
            options={
                'verbose_name': 'параметр свойства категории',
                'verbose_name_plural': 'параметры свойства категории',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(default='products_photo/default.png', upload_to='products_photo/', verbose_name='фото товара')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_photo', to='products.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'фото товара',
                'verbose_name_plural': 'фото товаров',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='properties',
            field=models.ManyToManyField(related_name='products', related_query_name='product', through='products.PropertyProduct', to='products.property', verbose_name='свойства товара'),
        ),
        migrations.AddField(
            model_name='category',
            name='properties',
            field=models.ManyToManyField(related_name='categories', related_query_name='category', through='products.PropertyCategory', to='products.property', verbose_name='свойства товаров в категории'),
        ),
        migrations.AddConstraint(
            model_name='propertyproduct',
            constraint=models.UniqueConstraint(fields=('product', 'property'), name='products_propertyproduct_prop_unique_in_product'),
        ),
        migrations.AddConstraint(
            model_name='propertycategory',
            constraint=models.UniqueConstraint(fields=('category', 'property'), name='products_propertycategory_prop_unique_in_category'),
        ),
    ]

# Generated by Django 4.1.4 on 2023-07-21 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Product', '0004_product_description_en_product_description_ru_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'verbose_name': 'Product Color', 'verbose_name_plural': 'Product Colors'},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'verbose_name': 'Product Image', 'verbose_name_plural': 'Product Images'},
        ),
        migrations.AlterModelOptions(
            name='productreview',
            options={'verbose_name': 'Product Review', 'verbose_name_plural': 'Product Reviews'},
        ),
        migrations.AlterModelOptions(
            name='productvariant',
            options={'verbose_name': 'Product Variant', 'verbose_name_plural': 'Product Variants'},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'verbose_name': 'Product Size', 'verbose_name_plural': 'Product Sizes'},
        ),
        migrations.AddField(
            model_name='brand',
            name='name_en',
            field=models.CharField(max_length=100, null=True, verbose_name='Brand Name'),
        ),
        migrations.AddField(
            model_name='brand',
            name='name_ru',
            field=models.CharField(max_length=100, null=True, verbose_name='Brand Name'),
        ),
        migrations.AddField(
            model_name='brand',
            name='name_tg',
            field=models.CharField(max_length=100, null=True, verbose_name='Brand Name'),
        ),
        migrations.AddField(
            model_name='category',
            name='title_en',
            field=models.CharField(max_length=100, null=True, verbose_name='Category Name'),
        ),
        migrations.AddField(
            model_name='category',
            name='title_ru',
            field=models.CharField(max_length=100, null=True, verbose_name='Category Name'),
        ),
        migrations.AddField(
            model_name='category',
            name='title_tg',
            field=models.CharField(max_length=100, null=True, verbose_name='Category Name'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='color',
            name='code',
            field=models.CharField(max_length=7, verbose_name='color code'),
        ),
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(max_length=50, verbose_name='color name'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Product.product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='stock_quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Stock Quantity'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Product.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], default=None, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='review',
            field=models.TextField(verbose_name='Review'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='user_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Profile.userlocation', verbose_name='User location'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='verified_purchase',
            field=models.BooleanField(default=False, verbose_name='Verified purchase'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.color', verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.size', verbose_name='Size'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='size',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Size Name'),
        ),
    ]

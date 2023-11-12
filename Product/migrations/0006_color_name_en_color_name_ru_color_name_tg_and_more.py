# Generated by Django 4.1.4 on 2023-07-22 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0005_alter_color_options_alter_productimage_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='name_en',
            field=models.CharField(max_length=50, null=True, verbose_name='color name'),
        ),
        migrations.AddField(
            model_name='color',
            name='name_ru',
            field=models.CharField(max_length=50, null=True, verbose_name='color name'),
        ),
        migrations.AddField(
            model_name='color',
            name='name_tg',
            field=models.CharField(max_length=50, null=True, verbose_name='color name'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product-variants/', verbose_name='image'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='inventory',
            field=models.PositiveIntegerField(default=0, help_text='Available stock for this variant', verbose_name='Inventory'),
        ),
        migrations.AddField(
            model_name='size',
            name='name_en',
            field=models.CharField(max_length=50, null=True, verbose_name='Size Name'),
        ),
        migrations.AddField(
            model_name='size',
            name='name_ru',
            field=models.CharField(max_length=50, null=True, verbose_name='Size Name'),
        ),
        migrations.AddField(
            model_name='size',
            name='name_tg',
            field=models.CharField(max_length=50, null=True, verbose_name='Size Name'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='sku',
            field=models.CharField(help_text='Stock Keeping Unit', max_length=50, unique=True),
        ),
    ]
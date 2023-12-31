# Generated by Django 4.1.4 on 2023-08-12 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0016_alter_productvariant_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcombination',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_c_color', to='Product.color', verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='productcombination',
            name='product_v',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_v_combination', to='Product.productvariant', verbose_name='ProductVariant'),
        ),
        migrations.AlterField(
            model_name='productcombination',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_c_size', to='Product.size', verbose_name='Size'),
        ),
    ]

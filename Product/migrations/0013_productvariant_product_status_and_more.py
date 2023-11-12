# Generated by Django 4.1.4 on 2023-08-10 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0012_remove_productvariant_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='product_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('rejected', 'Rejected'), ('published', 'Published')], default='in_review', max_length=10, verbose_name='Product Status'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='specification',
            field=models.TextField(blank=True, null=True, verbose_name='specification'),
        ),
    ]

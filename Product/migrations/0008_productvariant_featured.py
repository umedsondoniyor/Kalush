# Generated by Django 4.1.4 on 2023-07-23 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0007_productvariant_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='Featured'),
        ),
    ]

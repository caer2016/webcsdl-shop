# Generated by Django 3.1.7 on 2021-04-25 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_product_imagename'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='productType',
            field=models.CharField(default=None, max_length=16),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.4 on 2023-10-16 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_quantity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UploadedImage',
        ),
    ]

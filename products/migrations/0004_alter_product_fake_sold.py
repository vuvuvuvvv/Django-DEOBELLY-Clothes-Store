# Generated by Django 4.2.4 on 2023-10-02 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_view'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='fake_sold',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

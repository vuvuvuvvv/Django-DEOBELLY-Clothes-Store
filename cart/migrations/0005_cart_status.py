# Generated by Django 4.2.6 on 2023-10-23 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.IntegerField(choices=[(1, 'Hoạt động'), (0, 'Không hoạt động')], default=1),
        ),
    ]
# Generated by Django 4.2.4 on 2023-09-25 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='geolocation',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='termsandservices',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]

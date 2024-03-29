# Generated by Django 4.2.4 on 2023-10-18 11:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consignee_name', models.CharField(max_length=100)),
                ('tel', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Số điện thoại gồm 10 chữ số bắt đầu với 09, 08, 07, 05, 03', regex='^(09|08|07|05|03)\\d{8}$')])),
                ('BL_code', models.CharField(max_length=100, unique=True)),
                ('address', models.CharField(max_length=5000)),
                ('notes', models.CharField(max_length=5000)),
                ('total_price', models.DecimalField(decimal_places=0, max_digits=20)),
                ('products_id_and_quantity', models.CharField(max_length=5000)),
                ('status', models.IntegerField(choices=[(0, 'Thất bại'), (1, 'Thành công'), (2, 'Đang xử lý'), (3, 'Đang vận chuyển')], default=2)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart_order', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

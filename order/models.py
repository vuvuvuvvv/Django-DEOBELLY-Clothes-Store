from django.db import models
from accounts.models import User
from system.constant import *
from django.utils import timezone
from products.models import Product
from django.core.validators import RegexValidator
from datetime import datetime

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='cart_order')
    consignee_name = models.CharField(max_length=100)
    tel = models.CharField(
        max_length=10,  
        validators=[
            RegexValidator(
                regex=r'^(09|08|07|05|03)\d{8}$',
                message="Số điện thoại gồm 10 chữ số bắt đầu với 09, 08, 07, 05, 03",
            )
        ],
    )
    BL_code = models.CharField(max_length=100,unique=True)
    address = models.CharField(max_length=5000)
    notes = models.CharField(max_length=5000)
    total_price = models.DecimalField(max_digits=20, decimal_places=0)
    products_id_and_quantity = models.CharField(max_length=5000)
    status = models.IntegerField(default = ORDER_PROCESSING, choices=ORDER_STATUS_CHOICE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        self.BL_code = f'D-{self.user.username}-{datetime.now().strftime("%Y%m%d%H%M%S")}'
        super().save(*args, **kwargs)

    @classmethod
    def get_orders(cls, user_obj):
        get_orders,created = cls.objects.get_or_create(user = user_obj)
        orders = []
        pr_q = get_orders.products_id_and_quantity
        if pr_q:
            for val in pr_q.split(';'):
                try:
                    product = Product.get_product_by_id(int(val.split(':')[0]))
                    quantity = val.split(':')[1]
                    total_price = product.selling_price*int(val.split(':')[1])
                except Exception:
                    product = None
                    quantity = 0
                    total_price = 0
                item = {
                    'product':product,
                    'quantity': quantity,
                    'total_price': total_price
                }
                orders.append(item)
        return orders

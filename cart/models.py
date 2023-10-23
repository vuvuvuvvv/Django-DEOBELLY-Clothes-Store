from django.db import models
from accounts.models import User
from system.constant import *
from django.utils import timezone
from products.models import Product
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_cart')
    # Save data: "product_id":"quantity" -> "1:2;2:5;3:23;..."
    products_id_and_quantity = models.CharField(max_length=5000, blank=True)
    status = models.IntegerField(default = STATUS_ACTIVE, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    #pr_q: product_id and quantity
    @classmethod
    def get_carts(cls, user_obj):
        get_cart,created = cls.objects.get_or_create(user = user_obj,status=STATUS_ACTIVE)
        carts = []
        pr_q = get_cart.products_id_and_quantity
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
                carts.append(item)
        return carts
    
    @classmethod
    def get_pr_q(cls, user_obj):
        get_cart,created = cls.objects.get_or_create(user = user_obj, status=STATUS_ACTIVE)
        return get_cart.products_id_and_quantity

    @classmethod
    def get_buynow_cart(cls, user_obj):
        get_cart,created = cls.objects.get_or_create(user = user_obj,status=STATUS_INACTIVE)
        carts = []
        pr_q = get_cart.products_id_and_quantity
        if pr_q:
            try:
                product = Product.get_product_by_id(int(pr_q.split(':')[0]))
                quantity = pr_q.split(':')[1]
                total_price = product.selling_price*int(pr_q.split(':')[1])
            except Exception:
                product = None
                quantity = 0
                total_price = 0
            item = {
                'product':product,
                'quantity': quantity,
                'total_price': total_price
            }
            carts.append(item)
        return carts

        

        
    
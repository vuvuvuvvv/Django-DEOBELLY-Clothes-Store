from system.constant import *
from products.models import ProductType
from django.shortcuts import get_object_or_404
from cart.models import Cart
def layout_data(req):
    get_all_product_type = ProductType.get_all_product_type()
    if req.user.is_authenticated:
        get_carts = Cart.get_carts(user_obj= req.user)
        cart_quantity = len(get_carts)
    else:
        cart_quantity = False


    return {
        'ADMIN_MAIL' : ADMIN_MAIL,
        'COMPANY_ADDRESS' : COMPANY_ADDRESS,
        'PHONE_CONTACT' : PHONE_CONTACT,
        'SENDER_NAME': SENDER_NAME,
        'product_type' : get_all_product_type,
        'cart_quantity': cart_quantity
    }
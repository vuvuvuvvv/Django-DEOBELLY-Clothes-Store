from django import template
from system.function import encode,decode
from system.constant import TRACKING_STATUS
from products.models import Product
import locale

register = template.Library()

@register.filter(name='encrypt_string')
def encrypt_string(value):
    # Use your encryption logic here
    return encode(value)

@register.filter(name='split_string')
def split_string(arr, delimiter):
    return arr.split(delimiter)

@register.filter(name='format_number')
def format_number(val):
    return '{:,.0f}'.format(val).replace(',', '.')

@register.filter(name='get_order_information')
def get_order_information(pr_q):
    orders_list = []
    for val in pr_q.split(';'):
        try:
            product_name = Product.get_product_by_id(int(val.split(':')[0])).name
            quantity = val.split(':')[1]
        except Exception:
            product_name = None
            quantity = 0
        item = {
            'name':product_name,
            'quantity': quantity,
        }
    orders_list.append(item)
    return orders_list

@register.filter(name='tracking_status')
def tracking_status(status):
    return TRACKING_STATUS[str(status)]
from django import template
from system.function import encode,decode
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

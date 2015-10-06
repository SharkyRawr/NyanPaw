from django import template
from django.utils.safestring import SafeString

register = template.Library()

@register.filter(name='hex')
def filter_hex(val):
    return hex(val)

@register.filter(name='hexlify')
def filter_hexlify(val):
    return str(val).encode('hex')

@register.filter(name='stringify')
def filter_stringify(val):
    return repr(str(val))
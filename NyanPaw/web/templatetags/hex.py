from django import template
from django.utils.safestring import SafeString

register = template.Library()

@register.filter(name='hexlify')
def filter_hex(val):
    return str(val).encode('hex')

@register.filter(name='stringify')
def filter_str(val):
    return repr(str(val))
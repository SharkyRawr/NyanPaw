
import binascii
from django import template
from django.utils.safestring import SafeString

register = template.Library()

@register.filter(name='hex')
def filter_hex(val):
    return "0x%x" % val

@register.filter(name='hexlify')
def filter_hexlify(val):
    return binascii.hexlify(val)

@register.filter(name='stringify')
def filter_stringify(val):
    return repr(str(val))

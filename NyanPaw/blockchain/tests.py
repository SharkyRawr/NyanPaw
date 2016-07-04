from django.test import TestCase

from util import decode_address

# Create your tests here.

class TestPubkey(TestCase):
    def test_nyan_addr(self):
        shouldbe = "K9KSaN9iog5jyad6ofGCoXgnfRJrVCwY2s"
        addr = decode_address("2103991f733f9ed1f98310cf6f1e4864587841e7689989aff91a2559aeeda6ab2f56ac".decode('hex'), version=45)
        self.assertEquals(addr, shouldbe)

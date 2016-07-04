import hashlib
import binascii
import re


def calculate_target(nBits):
    return (nBits & 0xffffff) << (8 * ((nBits >> 24) - 3))


def target_to_difficulty(target):
    return ((1 << 224) - 1) * 1000 / (target + 1) / 1000.0


def calculate_difficulty(nBits):
    return target_to_difficulty(calculate_target(nBits))


def format_difficulty(diff):
    idiff = int(diff)
    ret = '.%03d' % (int(round((diff - idiff) * 1000)),)
    while idiff > 999:
        ret = (' %03d' % (idiff % 1000,)) + ret
        idiff = idiff / 1000
    return str(idiff) + ret


def decode_address(sig, version):
    from .base58 import b58encode

    if len(sig) != 35:
        raise ValueError("PubKey has wrong length", len(sig))

    # Step 2
    sha = hashlib.sha256(sig).digest()
    # Step 3
    ripe = hashlib.new('ripemd160', sha).digest()
    # Step 4
    ripe = chr(version) + ripe
    print(binascii.hexlify(ripe))
    # Step 5
    checksum = hashlib.sha256(hashlib.sha256(ripe).digest()).digest()[0:4]

    addr = ripe + checksum

    return b58encode(addr)


def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

ADDRESS_RE = re.compile('[1-9A-HJ-NP-Za-km-z]{26,}\\Z')


def possible_address(string):
    return ADDRESS_RE.match(string)


def hash_to_address(version, hash):
    vh = version + hash
    return base58.b58encode(vh + double_sha256(vh)[:4])


def decode_check_address(address):
    if possible_address(address):
        version, hash = decode_address(address)
        if hash_to_address(version, hash) == address:
            return version, hash
    return None, None


def decode_address(addr):
    bytes = base58.b58decode(addr, None)
    if len(bytes) < 25:
        bytes = ('\0' * (25 - len(bytes))) + bytes
    return bytes[:-24], bytes[-24:-4]

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

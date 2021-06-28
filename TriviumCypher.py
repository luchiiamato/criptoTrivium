from collections import deque
from itertools import repeat
from sys import version_info

_allbytes = dict([("%02X" % i, i) for i in range(256)])

def _hex_to_bytes(s):
    return [_allbytes[s[i:i+2].upper()] for i in range(0, len(s), 2)]

def hex_to_bits(s):
    return [(b >> i) & 1 for b in _hex_to_bytes(s)
            for i in range(8)]

def bits_to_hex(b):
    return "".join(["%02X" % sum([b[i + j] << j for j in range(8)])
                    for i in range(0, len(b), 8)])

def pixels_to_hex(data):
    hex = ''
    for (r, g, b) in data:
        hex += '%02x%02x%02x' % (r, g, b)
    return hex

def hex_to_rgb(data):
    res = list()
    for i in range(0, len(data), 6):
        hex_value = data[i:i+6]
        lv = len(hex_value)
        t = tuple(int(hex_value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        res.append(t)
    
    return res


class Trivium:
    def __init__(self, key, iv):
        self.state = None
        self.counter = 0
        self.key = key
        self.iv = iv

        # Initialize state
        # len 100
        init_list = list(map(int, list(self.key)))
        init_list += list(repeat(0, 20))
        # len 84
        init_list += list(map(int, list(self.iv)))
        init_list += list(repeat(0, 4))
        # len 111
        init_list += list(repeat(0, 108))
        init_list += list([1, 1, 1])
        self.state = deque(init_list)

        for i in range(4*288):
            self._gen_keystream()

    def __reset(self):
        # Initialize state
        # len 100
        init_list = list(map(int, list(self.key)))
        init_list += list(repeat(0, 20))
        # len 84
        init_list += list(map(int, list(self.iv)))
        init_list += list(repeat(0, 4))
        # len 111
        init_list += list(repeat(0, 108))
        init_list += list([1, 1, 1])
        self.state = deque(init_list)

        for i in range(4*288):
            self._gen_keystream()

    def encrypt(self, message):
        self.__reset()
        plaintext_bin = hex_to_bits(message)

        ciphertext = []
        
        for i in range(len(plaintext_bin)):
            ciphertext.append(self._gen_keystream() ^ plaintext_bin[i])

        return bits_to_hex(ciphertext)

    def decrypt(self, cipher):
        self.__reset()
        ciphertext_bin = []
        plaintext_bin = []
        if any(c.isalpha() for c in cipher):
            ciphertext_bin = hex_to_bits(cipher)
            for i in range(len(ciphertext_bin)):
                plaintext_bin.append(self._gen_keystream() ^ ciphertext_bin[i])
        
        plaintext_hex = bits_to_hex(plaintext_bin)
        return plaintext_hex

    def keystream(self):
        while self.counter < 2**64:
            self.counter += 1
            yield self._gen_keystream()

    def _setLength(self, input_data):
        input_data = "{0:080b}".format(input_data)
        if len(input_data) > 80:
            input_data = input_data[:(len(input_data)-81):-1]
        else:
            input_data = input_data[::-1]
        return input_data

    def _gen_keystream(self):
        a_1 = self.state[90] & self.state[91]
        a_2 = self.state[181] & self.state[182]
        a_3 = self.state[292] & self.state[293]

        t_1 = self.state[65] ^ self.state[92]
        t_2 = self.state[168] ^ self.state[183]
        t_3 = self.state[249] ^ self.state[294]

        out = t_1 ^ t_2 ^ t_3

        s_1 = a_1 ^ self.state[177] ^ t_1
        s_2 = a_2 ^ self.state[270] ^ t_2
        s_3 = a_3 ^ self.state[68] ^ t_3

        self.state.rotate(1)

        self.state[0] = s_3
        self.state[100] = s_1
        self.state[184] = s_2

        return out
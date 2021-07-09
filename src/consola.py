from TriviumCypher import Trivium, hex_to_bits, hex_to_rgb, pixels_to_hex

key = 'fdfdfdfdfdfdfdfdfdfdfd'
iv = 'bcbcbcbcbcbcbcbcbcbc'

cipher = Trivium(key, iv)

plaintext = 'Tomas Dal Verme'

hex_string = "".join("{:02x}".format(ord(c)) for c in plaintext).upper()

print('Texto plano ASCII: ', plaintext)
print('Texto plano hexadecimal: ', hex_string, '\n')

ciphertext = cipher.encrypt(hex_string)
print('Criptograma hexadecimal: ', ciphertext, '\n')

plaintext = cipher.decrypt(ciphertext)
print('Texto desencriptado hexadecimal: ', plaintext)

plaintext = bytearray.fromhex(plaintext).decode()
print('Texto desencriptado ASCII: ', plaintext)
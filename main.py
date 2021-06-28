from PIL import Image
from TriviumCypher import Trivium, hex_to_bits, hex_to_rgb, pixels_to_hex

key_hex = 'f0f0f0f0f0f0f0f0f0f0'
iv_hex = 'feaefeaefeaefeaefeae'
filename = 'test2.jpg'

KEY = hex_to_bits(key_hex)[::-1]
IV = hex_to_bits(iv_hex)[::-1]

if len(KEY) < 80:
    for k in range (80-len(KEY)):
        KEY.append(0)

if len(IV) < 80:
    for i in range (80-len(IV)):
        IV.append(0)

trivium = Trivium(KEY, IV)

with open(filename, 'rb') as f:
    content = f.read()

image = Image.open(filename)
data = list(image.getdata())
width, height = image.size

data = pixels_to_hex(data).upper()
ciphertext = trivium.encrypt(data)
data = hex_to_rgb(ciphertext)

image = Image.new("RGB", (width, height))
image.putdata(data)
image.save('cifrada.jpg')

data = pixels_to_hex(data)
plain = trivium.decrypt(data)
data = hex_to_rgb(plain)

image = Image.new("RGB", (width, height))
image.putdata(data)
image.save('descifrada.jpg')
import cv2
import binascii
from PIL import Image
from PIL.ExifTags import TAGS
import io
import base64
from trivium import *
from getpass import getpass
import sys



#key = 0xf0f0f0f0f0f0f0f0f0f0
#iv = 0xfeaefeaefeaefeaefeae
key = 0xf0f0f0f0f0f0f0f0f0f0
iv = 0xfeaefeaefeaefeaefeae
cipher = Trivium(key, iv)
"""
text = getpass("Ingresar Texto Plano:")
text = cipher.encode(text)
print("Texto codificado: " + text)
decision =  input("Quiere desencriptar el Mensaje?\t")
if decision == "S" or decision == "s" or decision == "si" or decision == "":
    desencriptar = Trivium(key, iv)
    text = desencriptar.encode(text)
    print("Texto decodificado: " + text)
"""




filename = 'test.jpg'
with open(filename, 'rb') as f:
    content = f.read()
exifdata = content._getexif()
print(exifdata)

contenido = binascii.hexlify(content)
filetxt = 'CipherImg.txt'
with open (filetxt, 'wb') as wr:
    wr.write(contenido)
with open (filetxt, 'r') as r:
    content2 = r.read()
text = cipher.encode(content2)
text1= str.encode(text)
with open ('CipherImage.jpg', 'wb') as wr:
    wr.write(text1)
desencriptar = Trivium(key, iv)
text = desencriptar.encode(text)
with open ('CipherImg2.txt', 'wt') as wr:
    wr.write(text)




"""
# iterating over all EXIF data fields

for tag_id in exifdata:
    # get the tag name, instead of human unreadable tag id
    tag = TAGS.get(tag_id, tag_id)
    data = exifdata.get(tag_id)
    # decode bytes 
    if isinstance(data, bytes):
        data = data.decode()
    print(f"{tag:25}: {data}")
 
"""
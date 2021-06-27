from trivium import *


key = 0xf0f0f0f0f0f0f0f0f0f0
iv = 0xfeaefeaefeaefeaefeae
desencriptar = Trivium(key, iv)
print("Ingrese texto codificado:  ")
text = input()
text = desencriptar.encode(text)
print("Texto decodificado: " + text)


import PySimpleGUI as sg
import os.path
import tempfile
from PIL import ImageTk, Image
from TriviumCypher import Trivium, hex_to_bits, hex_to_rgb, pixels_to_hex

key_hex = 'f0f0f0f0f0f0f0f0f0f0'
iv_hex = 'feaefeaefeaefeaefeae'

KEY = hex_to_bits(key_hex)[::-1]
IV = hex_to_bits(iv_hex)[::-1]

if len(KEY) < 80:
    for k in range (80-len(KEY)):
        KEY.append(0)

if len(IV) < 80:
    for i in range (80-len(IV)):
        IV.append(0)

trivium = Trivium(KEY, IV)
ciphertext = ''
width, height = 0, 0

# First the window layout in 2 columns
file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        ),
    ],
    [
        sg.Button("Cifrar", disabled=True, key="-CIFRAR-"),
    ],
]

image_viewer_column = [
    [sg.Text("Elegí una imagen en el panel de la izquierda:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
    [sg.Button("Descifrar", disabled=True, key="-DESCIFRAR-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image Viewer", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".jpg"))
        ]
        window["-FILE LIST-"].update(fnames)

    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            window["-DESCIFRAR-"].update(disabled=True)
            filename = values["-FOLDER-"] + "/" + values["-FILE LIST-"][0]
            window["-TOUT-"].update(values["-FILE LIST-"][0])
            img = ImageTk.PhotoImage(Image.open(filename))
            window["-IMAGE-"].update(data=img)
            window["-CIFRAR-"].update(disabled=False)
        except:
            pass
    
    elif event == "-CIFRAR-":
        try:
            filename = values["-FOLDER-"] + "/" + values["-FILE LIST-"][0]
            image = Image.open(filename)
            data = list(image.getdata())
            width, height = image.size

            data = pixels_to_hex(data).upper()
            ciphertext = trivium.encrypt(data)
            data = hex_to_rgb(ciphertext)

            image = Image.new("RGB", (width, height))
            image.putdata(data)
            path_cifrada = tempfile.gettempdir() + "/" + values["-FILE LIST-"][0]
            image.save(path_cifrada)
            image = ImageTk.PhotoImage(Image.open(path_cifrada))
            window["-IMAGE-"].update(data=image)
            
            folder = values["-FOLDER-"]
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f for f in file_list
                    if os.path.isfile(os.path.join(folder, f))
                    and f.lower().endswith((".jpg"))
            ]
            window["-FILE LIST-"].update(fnames)
            window["-DESCIFRAR-"].update(disabled=False)
        except Exception as e:
            print(e)

    elif event == "-DESCIFRAR-":
        try:
            plain = trivium.decrypt(ciphertext)
            data = hex_to_rgb(plain)

            image = Image.new("RGB", (width, height))
            image.putdata(data)
            path_descifrada = tempfile.gettempdir() + "/" + "descifrada.jpg"
            image.save(path_descifrada)
            image = ImageTk.PhotoImage(Image.open(path_descifrada))
            window["-IMAGE-"].update(data=image)
            
            folder = values["-FOLDER-"]
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f for f in file_list
                    if os.path.isfile(os.path.join(folder, f))
                    and f.lower().endswith((".jpg"))
            ]
            window["-FILE LIST-"].update(fnames)
            window["-DESCIFRAR-"].update(disabled=True)
        except Exception as e:
            print(e)

window.close()
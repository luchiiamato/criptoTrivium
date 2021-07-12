import PySimpleGUI as GUI
import os.path
from PIL import ImageTk, Image
from TriviumCypher import Trivium, hex_to_rgb, pixels_to_hex

def update_files():
    folder = values["-FOLDER-"]
    try:
        file_list = os.listdir(folder)
    except:
        file_list = []

    fnames = [
        f for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png"))
    ]
    window["-FILE LIST-"].update(fnames)

cipher = Trivium('', '')

key_hex = ''
iv_hex = ''

ciphertext = ''
width, height = 0, 0

GUI.theme('LightGreen')

row_1 = [
    [
        GUI.Text('Ingresa la key en hexadecimal:', size=(25, 1)),
        GUI.InputText(key="-KEY-", enable_events=True),
        GUI.Button('Aplicar', key='-APLICAR_KEY-', disabled=True)
    ],
]

row_2 = [
    [
        GUI.Text('Ingresa el IV en hexadecimal:', size=(25, 1)),
        GUI.InputText(key="-IV-", enable_events=True),
        GUI.Button('Aplicar', key='-APLICAR_IV-', disabled=True)
    ],
]

row_3 = [
    [
        GUI.Text("Carpeta:", size=(7, 1)),
        GUI.In(size=(26, 1), enable_events=True, key="-FOLDER-"),
        GUI.FolderBrowse(),
        GUI.VSeparator(color='white', pad=((9, 0),(0, 0))),
        GUI.Text("Elegí una imagen en el panel de la izquierda.", pad=((20, 0),(0, 0)))
    ],
]

row_4 = [
    [
        GUI.Listbox(
                values=[],
                enable_events=True,
                size=(42, 20),
                key="-FILE LIST-"
        ),
        GUI.VSeperator(color='white', pad=((15, 0),(0, 0))),
        GUI.Image(key="-IMAGE-"),
    ]
]

row_5 = [
    [
        GUI.VerticalSeparator(
            color='white', 
            pad=((338, 0), (0, 0))
        ),
        GUI.Button(
            "Cifrar", 
            disabled=True, 
            pad=((5, 0), (0, 0)), 
            key="-CIFRAR-"
        ),
        GUI.Button(
            "Descifrar",
            disabled=True,
            pad=((20, 0), (0, 0)),
            key="-DESCIFRAR-"
        ), 
        GUI.InputText(
            '',
            font=('Arial', 10, 'bold', 'italic'),
            readonly=True,
            disabled_readonly_background_color=GUI.theme_element_background_color(),
            border_width= 0,
            pad=((50, 0), (0, 0)),
            key="-STATUS-"
        )
    ],
]

layout = [
    [
        row_1,
        row_2,
        [GUI.HorizontalSeparator(color='white')],
        row_3,
        row_4,
        row_5
    ],
]

window = GUI.Window("Cifrador Trivium", layout)


if __name__ == '__main__':
    while True:
        event, values = window.read()
        if event == "Exit" or event == GUI.WIN_CLOSED:
            break

        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            update_files()

        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                window["-DESCIFRAR-"].update(disabled=True)
                filename = values["-FOLDER-"] + "/" + values["-FILE LIST-"][0]
                img = ImageTk.PhotoImage(Image.open(filename))
                window["-IMAGE-"].update(data=img)
                window["-CIFRAR-"].update(disabled=False)
                window["-DESCIFRAR-"].update(disabled=False)
            except:
                pass

        elif event == "-KEY-":  # A file was chosen from the listbox
            try:
                window["-KEY-"].update(background_color='red')
                if len(values['-KEY-']) == 20:
                    window["-KEY-"].update(background_color='green')
                    window["-APLICAR_KEY-"].update(disabled=False)
                else:
                    window["-APLICAR_KEY-"].update(disabled=True)
            except:
                pass

        elif event == "-IV-":  # A file was chosen from the listbox
            try:
                window["-IV-"].update(background_color='red')
                if len(values['-IV-']) == 20:
                    window["-IV-"].update(background_color='green')
                    window["-APLICAR_IV-"].update(disabled=False)
                else:
                    window["-APLICAR_IV-"].update(disabled=True)
            except:
                pass
        
        elif event == "-APLICAR_KEY-":
            try:
                key_hex = values["-KEY-"]
                int(key_hex, 16)
                cipher.set_key(key_hex)
                window["-KEY-"].update(background_color='white')
                window["-APLICAR_KEY-"].update(disabled=True)
            except ValueError:
                GUI.popup('Uno de los caracteres no es un hexadecimal valido', title='Hexadecimal invalido')

        elif event == "-APLICAR_IV-":
            try:
                iv_hex = values["-IV-"]
                int(iv_hex, 16)
                cipher.set_iv(iv_hex)
                window["-IV-"].update(background_color='white')
                window["-APLICAR_IV-"].update(disabled=True)
            except ValueError:
                GUI.popup('Uno de los caracteres no es un hexadecimal valido', title='Hexadecimal invalido')

        elif event == "-CIFRAR-":
            try:
                window["-STATUS-"].update(value='Cifrando...')
                window.Refresh()
                
                filename = values["-FOLDER-"] + "/" + values["-FILE LIST-"][0]
                image = Image.open(filename)
                image = image.convert("RGB")
                data = list(image.getdata())
                width, height = image.size
                data = pixels_to_hex(data).upper()

                ciphertext = cipher.encrypt(data)
                data = hex_to_rgb(ciphertext)

                image = Image.new("RGB", (width, height))
                image.putdata(data)
                path_cifrada = filename.replace('.png', ' (cifrada).png')
                image.save(path_cifrada, format='png')
                image = ImageTk.PhotoImage(Image.open(path_cifrada))
                window["-IMAGE-"].update(data=image)
                
                update_files()
                window["-DESCIFRAR-"].update(disabled=False)
                window["-STATUS-"].update(value='')
            except Exception as e:
                print(e)

        elif event == "-DESCIFRAR-":
            try:
                window["-STATUS-"].update(value='Descifrando...')
                window.Refresh()

                filename = values["-FOLDER-"] + "/" + values["-FILE LIST-"][0]
                image = Image.open(filename)
                image = image.convert("RGB")
                data = list(image.getdata())
                width, height = image.size

                data = pixels_to_hex(data).upper()
                plain = cipher.decrypt(data)
                data = hex_to_rgb(plain)

                image = Image.new("RGB", (width, height))
                image.putdata(data)
                path_descifrada = filename.replace('.png', ' (descifrada).png')
                image.save(path_descifrada, format='png')
                image = ImageTk.PhotoImage(Image.open(path_descifrada))
                window["-IMAGE-"].update(data=image)
                
                update_files()
                window["-DESCIFRAR-"].update(disabled=True)
                window["-STATUS-"].update(value='')
            except Exception as e:
                print(e)

    window.close()
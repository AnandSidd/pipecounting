import PySimpleGUI as sg
import os.path
from PIL import Image, ImageTk
import io

# First the window layout in 2 columns
def get_img_data(f, maxsize=(2000, 1080), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(40, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(80, 50), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(80, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
        sg.Button('Proceed'),
        sg.CButton('Cancel')
    ]
]

window = sg.Window("Image Viewer", layout)
win2_active= False
# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(data=get_img_data(filename, first=True))

        except:
            pass
    if event == 'Proceed'  and not win2_active:
        win2_active = True
        layout2 = [[sg.Text('Window 2')],       # note must create a layout from scratch every time. No reuse
                   [sg.Button('Exit')],
                   [sg.Image(data=get_img_data(filename, first=True))]]
        win2 = sg.Window('Window 2', layout2)
        while True:
            ev2, vals2 = win2.read()
            if ev2 == sg.WIN_CLOSED or ev2 == 'Exit':
                win2.close()
                win2_active = False
                window.UnHide()
                break
                                    
##    print(event)
window.close()

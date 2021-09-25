import PySimpleGUI as sg
import os.path
from PIL import Image, ImageTk
import numpy as np
import io
import cv2
import pipeprocess

name = 'Control'
global p1
global p2
global minr
global maxr
# First the window layout in 2 columns
ct = 0

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

def on_trackbar1(minradius):
    im1 = cv2.imread(f_name)
    global ct
    minr = minradius
    maxr = cv2.getTrackbarPos('maximum_radius', name)
    p1 = cv2.getTrackbarPos('param1', name)
    p2 = cv2.getTrackbarPos('param2', name)
    ct = pipeprocess.preprocess(im1, minr,maxr , p1,p2)
def on_trackbar2(maxradius):
    im1 = cv2.imread(f_name)
    global ct
    maxr = maxradius
    minr = cv2.getTrackbarPos('minimum_radius', name)
    p1 = cv2.getTrackbarPos('param1', name)
    p2 = cv2.getTrackbarPos('param2', name)
    ct = pipeprocess.preprocess(im1, minr,maxr, p1,p2)
def on_trackbar3(par1):
    im1 = cv2.imread(f_name)
    global ct
    p1 = par1
    maxr = cv2.getTrackbarPos('maximum_radius', name)
    minr = cv2.getTrackbarPos('minimum_radius', name)
    p2 = cv2.getTrackbarPos('param2', name)
    ct = pipeprocess.preprocess(im1, minr,maxr , p1,p2)
def on_trackbar4(par2):
    im1 = cv2.imread(f_name)
    global ct
    p2 = par2
    maxr = cv2.getTrackbarPos('maximum_radius', name)
    minr = cv2.getTrackbarPos('minimum_radius', name)
    p1 = cv2.getTrackbarPos('param1', name)
    ct = pipeprocess.preprocess(im1, minr,maxr , p1,p2)

def drawcircle(action, x, y, flags, *userdata):
    global ct
    img = cv2.imread('aa.jpg')
    cv2.imshow(name, img)
    if action == cv2.EVENT_LBUTTONDOWN:
        centre = (x,y)
        ct = ct+1
        cv2.circle(img , centre, 15, (0, 200, 0), 2)
        print("Count = ", ct)
    elif action == cv2.EVENT_RBUTTONDOWN:
        ct = ct-1
        centre = (x,y)
        cv2.circle(img , centre, 15, (0, 0, 255), 2)
        print("Count = ", ct)
    cv2.imshow(name, img)
    cv2.imwrite('aa.jpg', img)
    
def opencv_window(file_name):
    global f_name
    f_name = file_name
    button = [20,60,50,250]
    cv2.namedWindow(name,cv2.WINDOW_NORMAL)
##    cv2.resizeWindow(name, 1080, 720)
    control_image = np.zeros((80,300), np.uint8)
    control_image[button[0]:button[1],button[2]:button[3]] = 180
    cv2.putText(control_image, 'Button',(100,50),cv2.FONT_HERSHEY_PLAIN, 2,(0),3)

    #show 'control panel'
    cv2.createTrackbar('minimum_radius', name , 1, 100, on_trackbar1)
    cv2.createTrackbar('maximum_radius', name , 30, 100, on_trackbar2)
    cv2.createTrackbar('param1', name , 140, 250, on_trackbar3)
    cv2.createTrackbar('param2', name , 25, 250, on_trackbar4)
    cv2.setMouseCallback(name,drawcircle)
##    cv2.imshow(name, control_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

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
    if event == 'Proceed':
        opencv_window(filename)
                                    
##    print(event)
window.close()

import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog as fd


def select_images(extension_img: tuple[str]=('png', 'jpg', 'jpeg')):
    # Open files window and select images
    images_name = fd.askopenfilenames(initialdir='./', filetypes=(('All files', '*.*'), ('PNG image', '*.png'), ('JPG image', '*.jp*g')))
    print(images_name)
    # Leave only name file with extension
    images_name = [name.lower().split('/')[-1] for name in images_name]
    print(images_name)
    # Delete all files without correct extension
    images_name = [name for name in images_name if name.split('.')[-1] in extension_img]
    print(images_name)
    return images_name

def select_new_dir():
    new_dir_name = fd.askdirectory(title="Where to paste resized images? Select folder:")
    print(new_dir_name)


root = tb.Window(themename='superhero')
root.title('Window image resizer')
root.geometry('1000x500')


button_open_dir = tb.Button(root, bootstyle=INFO, text='Select images', command=select_images)
button_open_dir.pack()

button_open_dir = tb.Button(root, bootstyle=INFO, text='Select directory', command=select_new_dir)
button_open_dir.pack()



root.mainloop()

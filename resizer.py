import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog as fd
from PIL import Image, ImageOps
import os


def select_images(extension_img: tuple[str]=('png', 'jpg', 'jpeg')):
    # Open files window and select images
    global images_name
    images_name = fd.askopenfilenames(initialdir='./', filetypes=(('All files', '*.*'), ('PNG image', '*.png'), ('JPG image', '*.jp*g')))
    print(images_name)
    if not images_name:
        return 0

    # Delete all files without correct extension
    images_name = [name for name in images_name if name.lower().split('.')[-1] in extension_img]
    only_name_images = [name.split('/')[-1] for name in images_name]
    print(images_name)

    add_images_to_listbox(only_name_images)


def select_new_dir():
    global new_dir_name
    new_dir_name = fd.askdirectory(title="Where to paste resized images? Select folder:")
    print(new_dir_name)

def add_images_to_listbox(only_name_images):
    for img in only_name_images:
        size = str(int(os.stat(img).st_size / 1024)) + ' KB'
        files_list_tb.insert('', END, values=(img, size))


def resize_images(list_img_text: str, new_dir_name: str, max_px: int, des_ext: str='png'):
    max_length_vertical = 0
    max_length_horizontal = 0
    for img_text in list_img_text:
        # Load image with orientation
        image = ImageOps.exif_transpose(Image.open(img_text))

        width_img, height_img = image.size

        # Do new directory
        if not os.path.isdir(new_dir_name):
            os.mkdir(new_dir_name)

        # Check position image
        if width_img > height_img:
            scale = width_img / max_px
            width_img_resize = max_px
            height_img_resize = int(height_img / scale)
            if height_img_resize > max_length_vertical:
                max_length_vertical = height_img_resize
            if width_img_resize > max_length_horizontal:
                max_length_horizontal = width_img_resize

            img_resize = image.resize((width_img_resize, height_img_resize))
            new_image_name = (img_text.split("/")[-1]).split(".")[0]
            print(new_image_name)
            img_resize.save(f'{new_dir_name}/{new_image_name}.{des_ext}')

        else:
            scale = height_img / max_px
            height_img_resize = max_px
            width_img_resize = int(width_img / scale)
            if height_img_resize > max_length_vertical:
                max_length_vertical = height_img_resize
            if width_img_resize > max_length_horizontal:
                max_length_horizontal = width_img_resize

            img_resize = image.resize((width_img_resize, height_img_resize))
            new_image_name = (img_text.split("/")[-1]).split(".")[0]
            print(new_image_name)
            img_resize.save(f'{new_dir_name}/{new_image_name}.{des_ext}')



root = tb.Window(themename='superhero')
root.title('Window image resizer')
root.geometry('1000x500')

images_name = ''
new_dir_name = ''

labelframe_select = tb.Labelframe(root, bootstyle=INFO, text='Images to resize')
labelframe_select.pack(anchor=NW, padx=10, pady=10)

button_select_images = tb.Button(labelframe_select, bootstyle=INFO, text='Select images', command=select_images)
button_select_images.pack(padx=20, pady=5)

files_list_tb = tb.Treeview(labelframe_select, bootstyle=INFO, columns=('image', 'size'), show='headings')
files_list_tb.heading('image', text='Image')
files_list_tb.heading('size', text='Size')
files_list_tb.pack(side=LEFT)

select_scroll = tb.Scrollbar(labelframe_select, bootstyle=INFO, orient=VERTICAL, command=files_list_tb.yview)
files_list_tb.configure(yscrollcommand=select_scroll.set)
select_scroll.pack(side=RIGHT, fill=Y)
#file_list = tk.Listbox(labelframe_select, xscrollcommand=True, yscrollcommand=True)
#file_list.pack(padx=10, pady=5)
#file_list.xview_moveto(1)


button_select_new_dir = tb.Button(root, bootstyle=INFO, text='Select directory', command=select_new_dir)
button_select_new_dir.pack(padx=30)

button_resize = tb.Button(root, bootstyle=INFO, text='Resize images !!!', command=lambda: resize_images(images_name, new_dir_name, 200))
button_resize.pack(padx=30)

print(images_name)
# Image weight
print(int(os.stat('3.jpeg').st_size / 1024))





root.mainloop()

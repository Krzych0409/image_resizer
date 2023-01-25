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
    new_dir_name.set(fd.askdirectory(title="Where to paste resized images? Select folder:"))
    print(new_dir_name.get())

def add_images_to_listbox(only_name_images):
    for img in only_name_images:
        size = str(int(os.stat(img).st_size / 1024)) + ' KB'
        tree_img.insert('', END, values=(img, size))

def get_all_image_name():
    global name_img_list
    for item in tree_img.get_children():
        name_img_list.append(tree_img.set(item, 'image'))

    return name_img_list

def clear_img_treeview():
    for item in tree_img.get_children():
        tree_img.delete(item)


def resize_images(list_img_text: list[str], new_dir_name: str, max_px: int, des_ext: str='png'):
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
new_dir_name = tb.StringVar()
name_img_list = []


labelframe_select = tb.Labelframe(root, bootstyle=INFO, text='Images to resize')
labelframe_select.pack(anchor=NW, padx=10, pady=5)

button_select_images = tb.Button(labelframe_select, bootstyle=INFO+OUTLINE, text='Select images', command=select_images)
button_select_images.grid(row=0, column=0, pady=10)
button_clear_tree = tb.Button(labelframe_select, bootstyle=INFO+OUTLINE, text='Clear list', command=clear_img_treeview)
button_clear_tree.grid(row=0, column=1, columnspan=2, pady=10)

tree_img = tb.Treeview(labelframe_select, bootstyle=INFO, columns=('image', 'size'), show='headings')
tree_img.heading('image', text='Image')
tree_img.heading('size', text='Size')
tree_img.column('image', width=250, minwidth=200)
tree_img.column('size', width=60, minwidth=30)
tree_img.grid(row=1, column=0, columnspan=2)
select_scroll_x = tb.Scrollbar(labelframe_select, bootstyle=INFO, orient=HORIZONTAL, command=tree_img.xview)
select_scroll_y = tb.Scrollbar(labelframe_select, bootstyle=INFO, orient=VERTICAL, command=tree_img.yview)
tree_img.configure(xscrollcommand=select_scroll_x.set)
tree_img.configure(yscrollcommand=select_scroll_y.set)
select_scroll_x.grid(row=2, column=0, columnspan=2, sticky=W+E)
select_scroll_y.grid(row=1, column=2, sticky=N+S)


button_select_new_dir = tb.Button(labelframe_select, bootstyle=INFO+OUTLINE, text='Select directory', command=select_new_dir)
button_select_new_dir.grid(row=3, column=0, padx=5, pady=10, sticky=W)
label_select_new_dir = tb.Label(labelframe_select, textvariable=new_dir_name)
label_select_new_dir.grid(row=3, column=1)


button_resize = tb.Button(root, bootstyle=INFO+OUTLINE, text='Resize all images !!!', command=lambda: resize_images(get_all_image_name(), new_dir_name.get(), 200))
button_resize.pack(padx=30)



root.mainloop()

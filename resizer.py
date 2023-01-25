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

    add_images_to_listbox(only_name_images, images_name)

def add_images_to_listbox(only_name_images, images_name):
    for img, path in zip(only_name_images, images_name):
        size = str(int(os.stat(path).st_size / 1024)) + ' KB'
        tree_img.insert('', END, values=(img, size))

def clear_img_treeview():
    for item in tree_img.get_children():
        tree_img.delete(item)

def select_new_dir():
    global new_dir_name
    new_dir_name.set(fd.askdirectory(title="Where to paste resized images? Select folder:"))
    print(choice_method.get())
    print(meter_resize.amountusedvar.get())

def get_all_image_name():
    global name_img_list
    for item in tree_img.get_children():
        name_img_list.append(tree_img.set(item, 'image'))

    return name_img_list

def choice_resize_method():
    if choice_method.get() == '%':
        # Disable other resize method
        entry_max_px.delete(0, len(entry_max_px.get()))
        entry_max_px.configure(state=DISABLED)
        entry_precise_x.delete(0, len(entry_precise_x.get()))
        entry_precise_x.configure(state=DISABLED)
        entry_precise_y.delete(0, len(entry_precise_y.get()))
        entry_precise_y.configure(state=DISABLED)
        # Enable this method
        meter_resize.configure(interactive=True)

    elif choice_method.get() == 'max_px':
        # Disable other resize method
        meter_resize.configure(amountused=0)
        meter_resize.configure(interactive=False)
        entry_precise_x.delete(0, len(entry_precise_x.get()))
        entry_precise_x.configure(state=DISABLED)
        entry_precise_y.delete(0, len(entry_precise_y.get()))
        entry_precise_y.configure(state=DISABLED)
        # Enable this method
        entry_max_px.configure(state=NORMAL)

    elif choice_method.get() == 'xy':
        # Disable other resize method
        meter_resize.configure(amountused=0)
        meter_resize.configure(interactive=False)
        entry_max_px.delete(0, len(entry_max_px.get()))
        entry_max_px.configure(state=DISABLED)
        # Enable this method
        entry_precise_x.configure(state=NORMAL)
        entry_precise_y.configure(state=NORMAL)



    '''if choice_method.get() == 'meter':
        global meter_resize
        meter_resize = tb.Meter(labelframe_option, bootstyle=INFO, subtext='%', metersize=150, interactive=True, arcrange=180, arcoffset=180)
        meter_resize.grid(row=1, column=0)
    elif choice_method.get() == 'entry':
        meter_resize.destroy()
        entry = tb.Entry(labelframe_option, text=choice_method.get())
        entry.grid(row=1, column=0)
        print(choice_method.get())'''


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
#root.geometry('1000x500')

images_name = ''
new_dir_name = tb.StringVar()
name_img_list = []


# Frame - select images
labelframe_select = tb.Labelframe(root, bootstyle=INFO, text='Images to resize')
labelframe_select.grid(row=0, column=0, padx=10, pady=5, ipadx=0, ipady=0, sticky=N+S)

button_select_images = tb.Button(labelframe_select, bootstyle=INFO+OUTLINE, text='Select images', command=select_images)
button_select_images.grid(row=0, column=0, padx=5, pady=10, sticky=W)
button_clear_tree = tb.Button(labelframe_select, bootstyle=INFO+OUTLINE, text='Clear list', command=clear_img_treeview)
button_clear_tree.grid(row=0, column=1, padx=5, pady=10, sticky=W)

tree_img = tb.Treeview(labelframe_select, bootstyle=INFO, columns=('image', 'size'), show='headings')
tree_img.heading('image', text='Image')
tree_img.heading('size', text='Size')
tree_img.column('image', width=250, minwidth=200)
tree_img.column('size', width=60, minwidth=50)
tree_img.grid(row=1, column=0, columnspan=2)
select_scroll_x = tb.Scrollbar(labelframe_select, bootstyle=INFO+ROUND, orient=HORIZONTAL, command=tree_img.xview)
select_scroll_y = tb.Scrollbar(labelframe_select, bootstyle=INFO+ROUND, orient=VERTICAL, command=tree_img.yview)
tree_img.configure(xscrollcommand=select_scroll_x.set)
tree_img.configure(yscrollcommand=select_scroll_y.set)
select_scroll_x.grid(row=2, column=0, columnspan=2, sticky=W+E)
select_scroll_y.grid(row=1, column=2, sticky=N+S)
belt_select = tb.Panedwindow(labelframe_select, bootstyle=SECONDARY, orient=HORIZONTAL, height=5)
belt_select.grid(row=3, column=0, columnspan=3, pady=20, sticky=W+E)

button_select_new_dir = tb.Button(labelframe_select, bootstyle=INFO+OUTLINE, text='Select directory for new images', command=select_new_dir)
button_select_new_dir.grid(row=4, column=0, columnspan=3, padx=5, pady=10, sticky=N)
entry_select_new_dir = tb.Entry(labelframe_select, textvariable=new_dir_name)
entry_select_new_dir.grid(row=5, column=0, columnspan=3, padx=5, sticky=W+E)
new_dir_scroll_x = tb.Scrollbar(labelframe_select, bootstyle=INFO+ROUND, orient=HORIZONTAL, command=entry_select_new_dir.xview)
new_dir_scroll_x.grid(row=6, column=0, columnspan=3, padx=5, sticky=W+E)
entry_select_new_dir.configure(xscrollcommand=new_dir_scroll_x.set)

# Frame - options
labelframe_option = tb.Labelframe(root, bootstyle=INFO, text='Options')
labelframe_option.grid(row=0, column=1, padx=10, pady=5, ipadx=0, ipady=5, sticky=N+S)

choice_method = tb.StringVar()

radiobutton_meter = tb.Radiobutton(labelframe_option, bootstyle=PRIMARY+TOOLBUTTON+OUTLINE, text='Percentage', variable=choice_method,
                                   value='%', command=choice_resize_method)
radiobutton_meter.grid(row=0, column=0, padx=10, pady=5)
meter_value = tb.IntVar()
meter_resize = tb.Meter(labelframe_option, bootstyle=PRIMARY, metersize=130, textright='%', arcrange=320, arcoffset=110,
                        stripethickness=3, meterthickness=8)
meter_resize.grid(row=1, column=0)
belt_meter = tb.Panedwindow(labelframe_option, bootstyle=SECONDARY, orient=HORIZONTAL, height=3)
belt_meter.grid(row=2, column=0, pady=5, sticky=W+E)

radiobutton_px = tb.Radiobutton(labelframe_option, bootstyle=WARNING+TOOLBUTTON+OUTLINE, text='Longer side in px', variable=choice_method,
                                value='max_px', command=choice_resize_method)
radiobutton_px.grid(row=3, column=0, padx=5, pady=5)
entry_max_px = tb.Entry(labelframe_option, bootstyle=WARNING, state=DISABLED)
entry_max_px.grid(row=4, column=0, padx=5, pady=5)
belt_max_px = tb.Panedwindow(labelframe_option, bootstyle=SECONDARY, orient=HORIZONTAL, height=3)
belt_max_px.grid(row=5, column=0, pady=5, sticky=W+E)

radiobutton_method = tb.Radiobutton(labelframe_option, bootstyle=SUCCESS+TOOLBUTTON+OUTLINE, text='Precise size', variable=choice_method,
                                    value='xy', command=choice_resize_method)
radiobutton_method.grid(row=6, column=0, padx=10, pady=5)
frame_precise = tb.Frame(labelframe_option)
frame_precise.grid(row=7, column=0)
label_precise_x = tb.Label(frame_precise, bootstyle=SUCCESS, text='Width:')
label_precise_x.grid(row=0, column=0, padx=5)
entry_precise_x = tb.Entry(frame_precise, bootstyle=SUCCESS, state=DISABLED)
entry_precise_x.grid(row=0, column=1, pady=5)
label_px_x = tb.Label(frame_precise, bootstyle=SUCCESS, text='px')
label_px_x.grid(row=0, column=2, padx=5)


label_precise_y = tb.Label(frame_precise, bootstyle=SUCCESS, text='Height:')
label_precise_y.grid(row=1, column=0, padx=5)
entry_precise_y = tb.Entry(frame_precise, bootstyle=SUCCESS, state=DISABLED)
entry_precise_y.grid(row=1, column=1)
label_px_y = tb.Label(frame_precise, bootstyle=SUCCESS, text='px')
label_px_y.grid(row=1, column=2, padx=5)

button_resize = tb.Button(root, bootstyle=INFO+OUTLINE, text='Resize all images !!!', command=lambda: resize_images(get_all_image_name(), new_dir_name.get(), 200))
button_resize.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

sizegrip_main = tb.Sizegrip(root, bootstyle=INFO).grid(row=1, column=20, sticky=SE)









root.mainloop()

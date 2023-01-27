import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog as fd
from PIL import Image, ImageOps
import os
from tkinter import messagebox


def select_images(extension_img: tuple[str]=('png', 'jpg', 'jpeg')):
    # Open files window and select images
    images_name = fd.askopenfilenames(initialdir='./', filetypes=(('All files', '*.*'), ('PNG image', '*.png'), ('JPG image', '*.jp*g')))
    global all_file_path
    all_file_path += images_name
    all_file_path = list(dict.fromkeys(all_file_path))
    print(type(all_file_path))
    print(f'All file path: {all_file_path}')

    if not all_file_path:
        return 0

    # Delete all files without correct extension
    global images_path
    images_path = [image_p for image_p in all_file_path if image_p.lower().split('.')[-1] in extension_img]
    only_name_images = [name.split('/')[-1] for name in images_path]

    print(f'All images path: {images_path}')
    print(f'All images name: {only_name_images}')

    add_images_to_treeview(only_name_images, images_path)

def add_images_to_treeview(only_name_images, images_path):
    for i in tree_img.get_children():
        tree_img.delete(i)
    for img, path in zip(only_name_images, images_path):
        size = str(int(os.stat(path).st_size / 1024)) + ' KB'
        tree_img.insert('', END, values=(img, size))

def clear_img_treeview():
    for item in tree_img.get_children():
        tree_img.delete(item)
        global images_path, all_file_path
        images_path = []
        all_file_path = []

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
    button_resize.configure(state=NORMAL)
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

def change_state_entry_ext():
    if source_ext.get():
        entry_ext.delete(0, len(entry_ext.get()))
        entry_ext.configure(state=DISABLED)
    else:
        entry_ext.configure(state=NORMAL)

def create_messagebox(message_type, title, message):
    if message_type == "info":
        messagebox.showinfo(title, message)
    elif message_type == "warning":
        messagebox.showwarning(title, message)
    elif message_type == "error":
        messagebox.showerror(title, message)
    elif message_type == "question":
        messagebox.askyesno(title, message)
    else:
        print("Invalid message type")

def resize_images(method, list_img_text: list[str], new_dir_name: str, final_ext: str):
    print(final_ext)
    # If new dir path is empty
    if not new_dir_name or not os.path.isdir(new_dir_name):
        # Do Toplevel window
        create_messagebox('error', 'Invalid directory path', 'You did not provide a path to the folder or path is invalid')
        print('TopLevel warning dir path')
        return 0

    # If is not image in list
    if not list_img_text:
        # Do Toplevel window
        create_messagebox('error', 'No images', 'You did not select images')
        print('TopLevel warning image')
        return 0

    # Do new directory if not exist
    if not os.path.isdir(new_dir_name):
        os.mkdir(new_dir_name)

    progress_var = len(images_path)
    print(list_img_text)


    # If choice: percent method - meter
    if method == '%':
        percent = meter_resize.amountusedvar.get()
        if not percent:
            create_messagebox('error', 'Percentage scale = 0%', 'The percentage cannot be 0!\nHow many percent of the length is to have a new image?')
            return 0
        # Disable meter
        meter_resize.configure(interactive=False)

        print(percent)
        print(type(percent))

        for img_text in list_img_text:
            # Load image with orientation
            image = ImageOps.exif_transpose(Image.open(img_text))
            width_img, height_img = image.size

            # Set final extension
            if source_ext:
                extension = (img_text.split("/")[-1]).split(".")[-1]
            else:
                extension = final_ext

            # Count new values image X and Y in px
            new_width_img = int(width_img * percent / 100)
            new_height_img = int(height_img * percent / 100)

            # Resize image and save with final extension in select directory
            img_resize = image.resize((new_width_img, new_height_img))
            new_image_name = (img_text.split("/")[-1]).split(".")[0]
            img_resize.save(f'{new_dir_name}/{new_image_name}.{extension}')

            print(f'new image: {new_image_name}.{extension}')

        meter_resize.configure(interactive=True)

    # If choice: longer side in px
    elif method == 'max_px':
        try:
            max_px = int(entry_max_px.get())
        except:
            create_messagebox('error', 'Longer side = 0px!', 'Longer side cannot be 0px!')
            return 0
        # Disable entry widget
        entry_max_px.configure(state=DISABLED)
        max_length_vertical = 0
        max_length_horizontal = 0
        for img_text in list_img_text:
            # Load image with orientation
            image = ImageOps.exif_transpose(Image.open(img_text))
            width_img, height_img = image.size

            # Set final extension
            if source_ext.get():
                extension = (img_text.split("/")[-1]).split(".")[-1]
            else:
                extension = final_ext

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
                img_resize.save(f'{new_dir_name}/{new_image_name}.{extension}')

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
                img_resize.save(f'{new_dir_name}/{new_image_name}.{extension}')

            print(f'new image: {new_image_name}.{extension}')

        entry_max_px.configure(state=NORMAL)


    # If choise: precise size in px
    elif method == 'xy':
        try:
            new_width_img = int(entry_precise_x.get())
            new_height_img = int(entry_precise_y.get())
        except:
            create_messagebox('error', 'Width or height new image has 0px!', 'Width and height must be greater than 0px!')
            return 0
        # Disable 2 entry widgets
        entry_precise_x.configure(state=DISABLED)
        entry_precise_y.configure(state=DISABLED)

        for img_text in list_img_text:
            # Load image with orientation
            image = ImageOps.exif_transpose(Image.open(img_text))

            # Set final extension
            if source_ext:
                extension = (img_text.split("/")[-1]).split(".")[-1]
            else:
                extension = final_ext

            # Resize image and save with final extension in select directory
            img_resize = image.resize((new_width_img, new_height_img))
            new_image_name = (img_text.split("/")[-1]).split(".")[0]
            img_resize.save(f'{new_dir_name}/{new_image_name}.{extension}')

            print(f'new image: {new_image_name}.{extension}')

        entry_precise_x.configure(state=NORMAL)
        entry_precise_y.configure(state=NORMAL)

root = tb.Window(themename='superhero')
root.title('Window image resizer')
#root.geometry('1000x500')


new_dir_name = tb.StringVar()
choice_method = tb.StringVar()
meter_value = tb.IntVar()
source_ext = tb.BooleanVar()
ext_var = tb.StringVar()
progress_var = tb.IntVar()
images_path = []
all_file_path = []


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


radiobutton_meter = tb.Radiobutton(labelframe_option, bootstyle=PRIMARY+TOOLBUTTON+OUTLINE, text='percent', variable=choice_method,
                                   value='%', command=choice_resize_method, width=15)
radiobutton_meter.grid(row=0, column=0, padx=10, pady=5)

meter_resize = tb.Meter(labelframe_option, bootstyle=PRIMARY, metersize=130, textright='%', arcrange=320, arcoffset=110,
                        stripethickness=3, meterthickness=8)
meter_resize.grid(row=1, column=0)
belt_meter = tb.Panedwindow(labelframe_option, bootstyle=SECONDARY, orient=HORIZONTAL, height=3)
belt_meter.grid(row=2, column=0, pady=5, sticky=W+E)

radiobutton_max_px = tb.Radiobutton(labelframe_option, bootstyle=WARNING+TOOLBUTTON+OUTLINE, text='Longer side in px', variable=choice_method,
                                value='max_px', command=choice_resize_method, width=15)
radiobutton_max_px.grid(row=3, column=0, padx=5, pady=5)
entry_max_px = tb.Entry(labelframe_option, bootstyle=WARNING, state=DISABLED)
entry_max_px.grid(row=4, column=0, padx=5, pady=5)
belt_max_px = tb.Panedwindow(labelframe_option, bootstyle=SECONDARY, orient=HORIZONTAL, height=3)
belt_max_px.grid(row=5, column=0, pady=5, sticky=W+E)

radiobutton_xy = tb.Radiobutton(labelframe_option, bootstyle=SUCCESS+TOOLBUTTON+OUTLINE, text='Precise size', variable=choice_method,
                                    value='xy', command=choice_resize_method, width=15)
radiobutton_xy.grid(row=6, column=0, padx=10, pady=5)
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


# Frame - resize
labelframe_resize = tb.Labelframe(root, bootstyle=INFO, text='Resize')
labelframe_resize.grid(row=0, column=2, padx=10, pady=5, ipadx=0, ipady=5, sticky=N+S)

checkbutton_ext = tb.Checkbutton(labelframe_resize, bootstyle=INFO+ROUND+TOGGLE, text='Source extension', variable=source_ext, command=change_state_entry_ext)
checkbutton_ext.grid(row=0, column=0, padx=10, pady=5)

label_or = tb.Label(labelframe_resize, text='or')
label_or.grid(row=1, column=0, padx=10, pady=0)
label_ext = tb.Label(labelframe_resize, text='Write new extension e.g. "jpg"')
label_ext.grid(row=2, column=0, padx=10, pady=5)

entry_ext = tb.Entry(labelframe_resize, bootstyle=INFO, width=5, textvariable=ext_var)
entry_ext.grid(row=3, column=0, padx=10, pady=5)

belt_ext = tb.Panedwindow(labelframe_resize, bootstyle=SECONDARY, orient=HORIZONTAL, height=3)
belt_ext.grid(row=4, column=0, pady=10, sticky=W+E)

button_resize = tb.Button(labelframe_resize, bootstyle=INFO+OUTLINE, text='Resize all images !!!', state=DISABLED,
                          command=lambda: resize_images(choice_method.get(), images_path, new_dir_name.get(), ext_var.get()))
button_resize.grid(row=5, column=0, padx=10, pady=5)





frame_bottom = tb.Labelframe(root, bootstyle=INFO, text='Resize')
frame_bottom.grid(row=1, column=0)

progressbar = tb.Progressbar(root, bootstyle=DANGER+STRIPED, variable=progress_var)
progressbar.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=W+E)
#progressbar.configure(value=50)



sizegrip_main = tb.Sizegrip(root, bootstyle=INFO).grid(row=1, column=5, sticky=SE)







root.mainloop()

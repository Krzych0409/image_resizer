## Image resizer
Simple gui app to resize and extension images.

![GUI image](resizer.png)

### Table of contents
* [Requirements](#requirements)
* [Description](#description)

### Requirements library
Pillow==9.4.0
tk==0.1.0
ttkbootstrap==1.10.1

### Description
The program changes size of image and extension. You can leave the default extension or use your own, e.g. png, jpg.

Images are loaded using the 'exif_transpose()' method from the 'PIL' library. This ensures that images have the correct orientation.

There are three methods to choose from:
* 1. Percentage reduction of photo. The specified value is a percentage of original dimension of photo. The original proportions of photo are preserved.
* 2. Specifying the value in pixels of the longer side of photo. The original proportions of photo are preserved.
* 3. Specifying the exact values of the sides of photo. The original proportions are not preserved.

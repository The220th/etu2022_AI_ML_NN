# -*- coding: utf-8 -*-

"""
Скрипт, который сконвертирует све изображения в заданной папке dir_src в папку dir_dst по заданному правилу converter.

> python convert_img_to.py dir_src dir_dst
"""

import os
import sys
import PIL
from PIL import Image

def converter(pilimg: "Pillow image") -> "Pillow image":
    #need_width, need_height = 32, 32
    need_width, need_height = 224, 224
    MODE = 1
    if(MODE == 0):
        return pilimg.resize((need_width, need_height), PIL.Image.Resampling.NEAREST)
    elif(MODE == 1):
        # Do cна4АлА евого крадватной
        width, height = pilimg.size
        if(width == height):
            pass # do nothing
        elif(width > height):
            new_width, new_height = height, height
            left = (width - new_width)/2
            top = (height - new_height)/2
            right = (width + new_width)/2
            bottom = (height + new_height)/2
            pilimg = pilimg.crop((left, top, right, bottom))
        else:
            new_width, new_height = width, width
            left = (width - new_width)/2
            top = (height - new_height)/2
            right = (width + new_width)/2
            bottom = (height + new_height)/2
            pilimg = pilimg.crop((left, top, right, bottom))

        return pilimg.resize((need_width, need_height), PIL.Image.Resampling.NEAREST)
    else:
        return 5051

def getFilesList(dirPath: str) -> list:
    return [os.path.join(path, name) for path, subdirs, files in os.walk(dirPath) for name in files]

def getDirsList(dirPath: str) -> list:
    return [os.path.join(path, name) for path, subdirs, files in os.walk(dirPath) for name in subdirs]

if __name__ == "__main__":
    dir1 = os.path.abspath(sys.argv[1])
    dir2 = os.path.abspath(sys.argv[2])

    dirs_abs_1 = getDirsList(dir1)
    dirs_abs_1 = sorted(dirs_abs_1)
    for dir_i_1 in dirs_abs_1:
        dir_i_rel = os.path.relpath(dir_i_1, dir1)
        dir_i_2 = os.path.join(dir2, dir_i_rel)
        os.makedirs(dir_i_2)

    files = getFilesList(dir1)
    files = sorted(files)

    gi, N = 0, len(files)
    for file_i in files:
        file_i_rel = os.path.relpath(file_i, dir1)
        file_i_out = os.path.join(dir2, file_i_rel)
        print(f"({gi+1}/{N}) Converting \"{file_i}\" to \"{file_i_out}\" by converter... ", end="")
        imagepil = PIL.Image.open(file_i)
        imagepil.load()
        imagepil = converter(imagepil)
        imagepil = imagepil.convert("RGB")
        imagepil.save(file_i_out,"PNG")
        print("OK")

        gi+=1


'''
# Пример аугментации:

import PIL
from PIL import Image
from imgaug import augmenters as iaa
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio

seq = iaa.Sequential([
    iaa.Crop(px=(0, 16)), # crop images from each side by 0 to 16px (randomly chosen)
    iaa.Fliplr(0.5), # horizontally flip 50% of the images
    iaa.GaussianBlur(sigma=(0, 3.0)) # blur images with a sigma of 0 to 3.0
])
rotate = iaa.Affine(rotate=(-25, 25)) # rotate image
a = imageio.imread("123.jpg")

augmented_image = rotate.augment_images([a])


plt.figure(figsize=(10, 10))
ax = plt.subplot(3, 3, 1)
plt.imshow(augmented_image[0])
plt.axis("off")

ax = plt.subplot(3, 3, 2)
plt.imshow(a)
plt.axis("off")

plt.show()

'''

















import PIL
from PIL import Image as IM
from PIL import ImageDraw as IMD
from PIL import ImageTk

import tkinter as tk
from tkinter import Tk, Canvas

img = IM.open("Board_Layout.png")
width, height = img.size
img_res = img.resize((800, 600))

root = Tk()

canvas = Canvas(root, width=800, height=600)
canvas.pack()

canvas.image = ImageTk.PhotoImage(img_res)
canvas.create_image(0, 0, image=canvas.image, anchor='nw')

root.mainloop()

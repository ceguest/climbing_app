import numpy as np
import cv2
from tkinter import *
from PIL import Image, ImageTk

from PIL import ImageFile

NUMBERED_IMAGE = "static/Hold_Numbers_Markup.png"
BASE_IMAGE = "static/Board_Layout.png"

root = Tk()
root.title("Title")
root.geometry("600x600")
root.configure(background="black")


class Example(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)

        self.image = Image.open(f"./{BASE_IMAGE}")
        self.img_copy = self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


e = Example(root)
e.pack(fill=BOTH, expand=YES)

root.mainloop()

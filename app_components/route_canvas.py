from tkinter import Canvas
from PIL import ImageTk


class RouteCanvas:
    def __init__(
            self,
            width,
            height,
            row,
            column,
            rowspan,
            columnspan,
            parent
    ):
        self.canvas = Canvas(parent, width=width, height=height)
        self.canvas.grid(row=row, column=column, rowspan=rowspan,
                         columnspan=columnspan)

    def display_image_on_route_canvas(self, route_image):
        self.canvas.image = ImageTk.PhotoImage(route_image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

from tkinter import Canvas
from PIL import ImageTk
import image_utils

BASE_IMAGE = "static/Board_Layout.png"


class RouteCanvas:
    def __init__(
            self,
            parent_window
    ):
        self.parent_window = parent_window

        canvas_position = parent_window.route_canvas_position()

        self.canvas = Canvas(parent_window.root, width=parent_window.img_width, height=parent_window.img_height)
        self.canvas.grid(row=canvas_position.row, column=canvas_position.column, rowspan=canvas_position.rowspan,
                         columnspan=canvas_position.columnspan)

        self.base_image = image_utils.open_image_and_size(BASE_IMAGE, parent_window.img_width, parent_window.img_height)
        self.display_image_on_route_canvas(self.base_image)

    def display_image_on_route_canvas(self, route_image):
        self.canvas.image = ImageTk.PhotoImage(route_image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

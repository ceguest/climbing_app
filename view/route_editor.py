from tkinter import Tk, Toplevel

import cv2
from model.hold_handler import HoldHandler


def create_base_img(self):
    hold_handler = HoldHandler()
    img = cv2.imread('static/Board_Layout.png', 1)
    all_hold_ids = self.hold_handler.get_all_hold_ids()
    holds = hold_handler.get_holds(all_hold_ids)
    for hold_id in holds.values():
        cv2.circle(img, (hold_id.x_coord, hold_id.y_coord),
                   20, (0, 0, 255), -1)

    cv2.rectangle(img, (1300, 2400), (2700, 3000), (0, 0, 0), -1)

    return img


class WidgetPosition:
    def __init__(self, row, column, rowspan, columnspan):
        self.row = row
        self.column = column
        self.rowspan = rowspan
        self.columnspan = columnspan


class RouteEditorWindow:
    def __init__(self):
        self.root = Toplevel()
        self.root.title('Route Editor')

        self.root.state('zoomed')
        # self.root.attributes('-zoomed', True)
        # self.root.geometry('520x300')
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        self.setup_window_grid()

    def setup_window_grid(self):
        self.img_height = 1000 #4032×3024
        self.img_width = self.img_height / 0.75  # Maintains 4:3 ratio

    def route_canvas_position(self):
        return WidgetPosition(
            row=0,
            column=0,
            rowspan=1,
            columnspan=1
        )

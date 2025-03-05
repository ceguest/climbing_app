from tkinter import *
from tkinter import messagebox
from route_adder import RouteAdder
from route_handler import RouteHandler
from route_visualiser import RouteVisualiser
from PIL import Image as IM
from PIL import ImageTk
import cv2
import image_utils
from app_components.route_canvas import RouteCanvas
from app_components.routes_listbox import RoutesListbox
from app_components.grades_filter_listbox import GradesFilterListbox
from app_components.option_buttons import OptionButtons
from app_components.main_window import MainWindow

NUMBERED_IMAGE = "static/Hold_Numbers_Markup.png"
BASE_IMAGE = "static/Board_Layout.png"


class TkApp:
    def __init__(self, route_handler, route_visualiser):
        self.route_handler = route_handler
        self.route_visualiser = route_visualiser

        self.main_window = MainWindow()
        self.root = self.main_window.root

        self.canvas = RouteCanvas(self.main_window)

        self.routes_listbox = RoutesListbox(
            self.route_handler,
            self.route_visualiser,
            self.canvas,
            self.main_window
        ).routes_listbox

        self.grades_listbox_class = GradesFilterListbox(
            self.route_handler,
            self.routes_listbox,
            self.main_window
        )
        self.grades_listbox = self.grades_listbox_class.grades_listbox

        self.option_buttons = OptionButtons(
            self.route_handler,
            self.grades_listbox_class,
            self.main_window
        )

        self.root.update_idletasks()
        self.root.resizable(0, 0)


if __name__ == "__main__":
    route_handler = RouteHandler()
    route_visualiser = RouteVisualiser()
    tk_app = TkApp(route_handler, route_visualiser)
    tk_app.root.mainloop()

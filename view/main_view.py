from tkinter import Canvas

import image_utils
from .grades_filter_listbox import GradesFilterListbox
from .option_buttons import OptionButtons
from .route_canvas import RouteCanvas
from .main_window import MainWindow
from .route_editor import RouteEditorWindow
from .route_menu import RouteMenu
from .routes_listbox import RoutesListbox
from PIL import ImageTk

class View:
    def __init__(self, controller):
        self.controller = controller

        self.route_menu = None

        self.main_window = MainWindow()
        self.root = self.main_window.root

        self.canvas = RouteCanvas(self.main_window)

        self.routes_listbox = RoutesListbox(
            self.controller,
            self.main_window
        )

        self.grades_listbox_class = GradesFilterListbox(
            self.controller,
            self.main_window
        )
        self.grades_listbox = self.grades_listbox_class.grades_listbox

        self.option_buttons = OptionButtons(
            self.controller.route_handler,
            self.grades_listbox_class,
            self.main_window,
            self.controller
        )

        self.root.update_idletasks()
        self.root.resizable(0, 0)

    def run_route_menu(self):
        self.route_menu = RouteMenu(self.controller)

    def run_route_editor(self, image=None):
        self.main_window.root.withdraw()
        self.route_editor_window = RouteEditorWindow()
        self.editor_canvas = RouteCanvas(self.route_editor_window, controller=self.controller, clickable=True)
        if image:
            self.editor_canvas.display_image_on_route_canvas(image)



        #
        # self.route_editor_window.root.update_idletasks()
        # self.route_editor_window.root.resizable(0, 0)
        # self.route_editor_window.root.mainloop()


if __name__ == "__main__":
    pass

from tkinter import Tk


class WidgetPosition:
    def __init__(self, row, column, rowspan, columnspan):
        self.row = row
        self.column = column
        self.rowspan = rowspan
        self.columnspan = columnspan

class MainWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title('Homewall')

        self.root.state('zoomed')
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        self.setup_window_grid()

    def setup_window_grid(self):
        self.img_height = self.height
        self.img_width = self.img_height / 0.75  # Maintains 4:3 ratio
        self.list_width = self.width - self.img_width

        self.routes_height = 0.6 * self.height
        self.grades_height = 0.2 * self.height
        self.buttons_height = 0.1 * self.height

        self.root.rowconfigure(0, minsize=self.routes_height)
        self.root.rowconfigure(1, minsize=self.grades_height)

        self.root.columnconfigure(0, minsize=self.img_width)
        self.root.columnconfigure(1, minsize=self.list_width)

    def route_canvas_position(self):
        return WidgetPosition(
            row=0,
            column=0,
            rowspan=3,
            columnspan=1
        )

    def routes_listbox_position(self):
        return WidgetPosition(
            row=0,
            column=1,
            rowspan=1,
            columnspan=1
        )

    def grades_listbox_position(self):
        return WidgetPosition(
            row=1,
            column=1,
            rowspan=1,
            columnspan=1
        )

    def option_buttons_position(self):
        return WidgetPosition(
            row=2,
            column=1,
            rowspan=1,
            columnspan=1
        )


from tkinter import (
    Frame,
    Label,
    SINGLE,
    Listbox,
    Scrollbar,
    N, E, S, W
)
from tkinter import END

from view.main_window import MainWindow


class RoutesListbox:
    def __init__(
            self,
            controller,
            parent_window: MainWindow,
    ):
        self.parent_window = parent_window
        route_listbox_position = parent_window.routes_listbox_position()

        self.img_height = parent_window.img_height
        self.img_width = parent_window.img_width
        self.controller = controller

        self.route_entry_frame = Frame(parent_window.root, width=parent_window.list_width,
                                       height=parent_window.routes_height)
        self.route_entry_frame.grid_propagate(0)
        self.route_entry_frame.rowconfigure(1, weight=1)
        self.route_entry_frame.columnconfigure(0, weight=1)

        route_entry_label = Label(self.route_entry_frame, text="Select route:")
        route_entry_label.grid(row=0, column=0, rowspan=1, columnspan=1)

        self.routes_listbox = Listbox(self.route_entry_frame, selectmode=SINGLE,
                                      exportselection=False)

        self.display_route_strings(controller.get_route_strings())

        self.routes_listbox.grid_propagate(0)
        self.routes_listbox.grid(row=1, column=0, rowspan=1, sticky='NESW')
        self.routes_listbox.bind("<<ListboxSelect>>", self.update_route)
        self.routes_listbox.bind("<Down>", self.OnEntryUpDown_routes_listbox)
        self.routes_listbox.bind("<Up>", self.OnEntryUpDown_routes_listbox)

        self.route_entry_frame.grid(
            row=route_listbox_position.row,
            column=route_listbox_position.column,
            rowspan=route_listbox_position.rowspan,
            columnspan=route_listbox_position.columnspan,
            sticky='NESW'
        )

        self.routes_scrollbar = Scrollbar(self.route_entry_frame,
                                          orient='vertical')
        self.routes_scrollbar.config(command=self.routes_listbox.yview)
        self.routes_scrollbar.grid(row=1, column=1, rowspan=1, columnspan=1,
                                   sticky=(N, E, S, W), padx=(0, 10))
        self.routes_listbox.config(yscrollcommand=self.routes_scrollbar.set)

    def display_route_strings(self, route_strings: list[str]):
        self.routes_listbox.delete(0, END)
        x = 1

        for route_string in route_strings:
            self.routes_listbox.insert(x, route_string)
            x += 1

    def OnEntryUpDown_routes_listbox(self, event):
        selection = event.widget.curselection()[0]

        if event.keysym == 'Up':
            selection += -1

        if event.keysym == 'Down':
            selection += 1

        if 0 <= selection < event.widget.size():
            event.widget.selection_clear(0, END)
            event.widget.select_set(selection)
        self.update_route()

    def update_route(self, event=None):
        route_index = self.routes_listbox.curselection()

        route_string = self.routes_listbox.get(route_index)
        route_id = int(route_string.split(":")[0])
        self.controller.update_current_route(route_id)

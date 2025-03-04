from tkinter import (
    Frame,
    Label,
    SINGLE,
    Listbox,
    Scrollbar,
    N, E, S, W
)

class RoutesListbox:
    def __init__(
            self,
            width,
            height,
            row,
            column,
            rowspan,
            columnspan,
            route_handler,
            parent
    ):
        self.route_entry_frame = Frame(parent, width=width,
                                       height=height)
        self.route_entry_frame.grid_propagate(0)
        self.route_entry_frame.rowconfigure(1, weight=1)
        self.route_entry_frame.columnconfigure(0, weight=1)

        route_entry_label = Label(self.route_entry_frame, text="Select route:")
        route_entry_label.grid(row=0, column=0, rowspan=1, columnspan=1)

        self.routes_listbox = Listbox(self.route_entry_frame, selectmode=SINGLE,
                                      exportselection=False)

        x = 1

        for index in route_handler.routes_df.index:
            list_string = f"{route_handler.routes_df['route_id'][index]}: {route_handler.routes_df['route_name'][index]} ({route_handler.routes_df['grade'][index]})"
            self.routes_listbox.insert(x, list_string)
            x += 1
        self.routes_listbox.grid_propagate(0)
        self.routes_listbox.grid(row=1, column=0, rowspan=1, sticky='NESW')
        self.routes_listbox.bind("<<ListboxSelect>>", self.update_route)
        self.routes_listbox.bind("<Down>", self.OnEntryUpDown_routes_listbox)
        self.routes_listbox.bind("<Up>", self.OnEntryUpDown_routes_listbox)

        self.route_entry_frame.grid(row=row, column=column, rowspan=rowspan,
                                    columnspan=columnspan, sticky='NESW')

        self.routes_scrollbar = Scrollbar(self.route_entry_frame,
                                          orient='vertical')
        self.routes_scrollbar.config(command=self.routes_listbox.yview)
        self.routes_scrollbar.grid(row=1, column=1, rowspan=1, columnspan=1,
                                   sticky=(N, E, S, W), padx=(0, 10))
        self.routes_listbox.config(yscrollcommand=self.routes_scrollbar.set)
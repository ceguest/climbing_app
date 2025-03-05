from tkinter import Frame, Label, Listbox, MULTIPLE, Scrollbar, N, E, S, W, END

class GradesFilterListbox:
    def __init__(
            self,
            route_handler,
            routes_listbox,
            parent_window
    ):
        parent_window = parent_window
        grades_listbox_position = parent_window.grades_listbox_position()
        self.routes_listbox = routes_listbox
        self.route_handler = route_handler
        self.grade_entry_frame = Frame(parent_window.root, width=parent_window.list_width,
                                       height=parent_window.grades_height)
        self.grade_entry_frame.grid_propagate(0)
        self.grade_entry_frame.rowconfigure(1, weight=1)
        self.grade_entry_frame.columnconfigure(0, weight=1)
        grade_entry_label = Label(self.grade_entry_frame, text="Select grades:")
        grade_entry_label.grid(row=0, column=0, rowspan=1, columnspan=1)
        self.grades = route_handler.get_sorted_grades()
        # sorted_grades = self.sort_grade_list()

        self.grades_listbox = Listbox(self.grade_entry_frame,
                                      selectmode=MULTIPLE,
                                      exportselection=False)
        x = 1
        for grade in self.grades:
            self.grades_listbox.insert(x, grade)
            x += 1
        self.grades_listbox.grid(row=1, column=0, rowspan=1, columnspan=1,
                                 sticky=(N, E, S, W))
        self.grades_listbox.bind("<<ListboxSelect>>", self.update_routes_listbox)

        self.grade_entry_frame.grid(
            row=grades_listbox_position.row,
            column=grades_listbox_position.column,
            rowspan=grades_listbox_position.rowspan,
            columnspan=grades_listbox_position.columnspan,
            sticky=(N, E, S, W)
        )

        self.grades_scrollbar = Scrollbar(self.grade_entry_frame,
                                          orient='vertical')
        self.grades_scrollbar.config(command=self.grades_listbox.yview)
        self.grades_scrollbar.grid(row=1, column=1, rowspan=1, columnspan=1,
                                   sticky=(N, E, S, W), padx=(0, 10))
        self.grades_listbox.config(yscrollcommand=self.grades_scrollbar.set)

    def update_routes_listbox(self, event=None):
        grade_indices = self.grades_listbox.curselection()
        grades = []
        for index in grade_indices:
            grades.append(self.grades_listbox.get(index))
        routes = self.route_handler.get_filtered_routes(grades=grades)
        self.routes_listbox.delete(0, END)
        x = 1
        for index in routes.index:
            list_string = f"{routes['route_id'][index]}: {routes['route_name'][index]} ({routes['grade'][index]})"
            self.routes_listbox.insert(x, list_string)
            x += 1

    def update_grades_listbox(self):
        self.grades_listbox.delete(0, END)
        self.grades = self.route_handler.get_sorted_grades()
        x = 1
        for grade in self.grades:
            self.grades_listbox.insert(x, grade)
            x += 1
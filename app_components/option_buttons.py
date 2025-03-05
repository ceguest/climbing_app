from tkinter import Frame, Button, LEFT, RIGHT, Tk, messagebox, END
from route_adder import RouteAdder

class OptionButtons:
    def __init__(
        self,
        route_handler,
        grades_listbox_class,
        parent_window
    ):
        options_button_position = parent_window.option_buttons_position()
        self.route_menu = None
        self.grades_listbox_class = grades_listbox_class
        self.route_handler = route_handler
        self.parent = parent_window.root
        button_frame = Frame(parent_window.root, width=parent_window.list_width,
                             height=parent_window.buttons_height)
        button_frame.grid_propagate(0)

        add_route_button = Button(button_frame, text="Route Menu",
                                  command=self.run_route_menu)
        add_route_button.pack(side=LEFT, padx=parent_window.list_width / 20)

        quit_button = Button(button_frame, text='Quit',
                             command=self.quit)
        quit_button.pack(side=RIGHT, padx=parent_window.list_width / 20)

        button_frame.grid(
            row=options_button_position.row,
            column=options_button_position.column,
            rowspan=options_button_position.rowspan,
            columnspan=options_button_position.columnspan,
            sticky='NESW'
        )

    def quit(self):
        self.parent.destroy()
        if self.route_menu: # TODO throws error if window has already been opened and closed
            self.route_menu.destroy()

    def run_route_menu(self):
        self.route_menu = Tk()
        self.route_menu.title('Menu')
        self.route_menu.geometry('200x200')

        add_route_button = Button(self.route_menu, text="Add route",
                                  command=self.add_route)
        add_route_button.pack(pady=20)

        edit_route_button = Button(self.route_menu, text="Edit route",
                                   command=self.edit_route)
        edit_route_button.pack(pady=20)

    def edit_route(self):
        self.route_menu.destroy()
        route_adder = RouteAdder(self.route_handler)
        route_adder.load_existing_route()
        route_adder.create_route()

        check_route_exists, route_nr, route_name = route_adder.check_route_exists()
        if check_route_exists == True and self.route_handler.currently_selected_route.id != route_nr:
            info_message = ('The holds you have selected already form route number ' +
                            str(route_nr) + " - " + route_name +
                            ' so this route edit cannot be saved.')
            info = messagebox.showwarning(title=None,
                                          message=info_message)

        else:
            check_add_route = messagebox.askquestion(title=None,
                                                     message='Do you want to save your new route?',
                                                     icon='question',
                                                     type='yesno',
                                                     default='yes')
            if check_add_route == 'yes': # TODO the "no" option may not work
                route_adder.update_route()
        self.parent.deiconify()
        self.route_handler.read_routes()
        self.grades_listbox_class.update_routes_listbox()

        self.grades_listbox_class.grades_listbox.delete(0, END)
        self.grades = self.route_handler.get_sorted_grades()
        # sorted_grades = self.sort_grade_list()
        x = 1
        for grade in self.grades:
            self.grades_listbox_class.grades_listbox.insert(x, grade)
            x += 1

    def add_route(self):
        self.route_menu.destroy()
        self.parent.withdraw()
        route_adder = RouteAdder()
        route_adder.create_route()
        check_route_exists, route_nr, route_name = route_adder.check_route_exists()
        if check_route_exists == True:
            info_message = ('The holds you have selected already form route number ' +
                            str(route_nr) + " - " + route_name +
                            ' so your new route cannot be created.')
            info = messagebox.showwarning(title=None,
                                          message=info_message)
        else:
            check_add_route = messagebox.askquestion(title=None,
                                                     message='Do you want to save your new route?',
                                                     icon='question',
                                                     type='yesno',
                                                     default='yes')
            if check_add_route == 'yes':
                route_adder.append_route()
        self.parent.deiconify()
        self.route_handler.read_routes()
        self.grades_listbox_class.update_routes_listbox()
        self.grades_listbox_class.update_grades_listbox()

from tkinter import *
from tkinter import messagebox
from route_adder import RouteAdder
from route_handler import RouteHandler
from route_visualiser import RouteVisualiser
from PIL import Image as IM
from PIL import ImageTk
import cv2

NUMBERED_IMAGE = "static/Hold_Numbers_Markup.png"
BASE_IMAGE = "static/Board_Layout.png"


class TkApp:
    def __init__(self, route_handler, route_visualiser):
        self.img_res = None
        self.canvas = None
        self.routes_listbox = None

        self.route_handler = route_handler
        self.route_visualiser = route_visualiser
        self.root = Tk()
        self.root.title('Homewall')

        self.get_window_dims()
        self.setup_window_grid()

        self.create_route_canvas(row=0, column=0, rowspan=3, columnspan=1)
        self.base_image = self.get_base_image()
        self.display_image_on_route_canvas(self.base_image)

        self.create_routes_listbox(row=0, column=1, rowspan=1, columnspan=1)

        self.create_grade_filter(row=1, column=1, rowspan=1, columnspan=1)

        self.create_buttons(row=2, column=1, rowspan=1, columnspan=1)

        self.root.update_idletasks()

    def get_window_dims(self):
        self.root.attributes('-fullscreen',True)
        self.root.resizable(width = False, height = False)
        self.root.update_idletasks()
        self.window_width = self.root.winfo_width()
        self.window_height = self.root.winfo_height()

    def setup_window_grid(self):
        self.img_height = self.window_height
        self.img_width = self.img_height / 0.75 # Maintains 4:3 ratio
        self.list_width = self.window_width - self.img_width

        self.routes_height = 0.6 * self.window_height
        self.grades_height = 0.2 * self.window_height
        self.buttons_height = 0.1 * self.window_height

        self.root.rowconfigure(0, minsize = self.routes_height)
        self.root.rowconfigure(1, minsize = self.grades_height)

        self.root.columnconfigure(0, minsize = self.img_width)
        self.root.columnconfigure(1, minsize = self.list_width)

    def get_base_image(self):
        img = IM.open(BASE_IMAGE)
##        width, height = img.size
        img_res = img.resize((int(self.img_width), int(self.img_height)))
        return img_res


    def convert_cv2_to_pil(self, img):
        # Rearrange the color channel
        b, g, r = cv2.split(img)
        img = cv2.merge((r, g, b))

        # Convert the cv2 Image object into a tk Image object
        im = IM.fromarray(img)
        return im

    def add_route(self):
        self.root.attributes('-fullscreen',False)
        self.root.withdraw()
        route_adder = RouteAdder()
        route_adder.create_route()
        check_route_exists, route_nr, route_name = route_adder.check_route_exists()
        if check_route_exists == True:
            info_message = ('The holds you have selected already form route number '+
                            str(route_nr) + " - " + route_name +
                            ' so your new route cannot be created.')
            info = messagebox.showwarning(title = None,
                                          message = info_message)
        else:
            check_add_route = messagebox.askquestion(title=None,
                                                     message='Do you want to save your new route?',
                                                     icon='question',
                                                     type='yesno',
                                                     default='yes')
            if check_add_route == 'yes':
                route_adder.append_route()
        self.root.deiconify()
        self.root.attributes('-fullscreen',True)
        self.route_handler.read_routes()
        self.update_routes_listbox()
        self.grades_listbox.destroy()
        self.create_grade_filter(row=31, column=3, rowspan=18, columnspan=1)
        self.root.update_idletasks()

    def create_route_canvas(self, row, column, rowspan, columnspan):
        self.canvas = Canvas(self.root, width=self.img_width,
                             height=self.img_height)
        self.canvas.grid(row=row, column=column, rowspan=rowspan,
                         columnspan=columnspan)

    def create_routes_listbox(self, row, column, rowspan, columnspan):

        self.route_entry_frame = Frame(self.root, width = self.list_width,
                                       height = self.routes_height)
        self.route_entry_frame.grid_propagate(0)
        self.route_entry_frame.rowconfigure(1, weight=1)
        
        route_entry_label = Label(self.route_entry_frame, text="Select route:")
        route_entry_label.grid(row=0, column=0, rowspan=1, columnspan=1)

        self.routes_listbox = Listbox(self.route_entry_frame, selectmode=SINGLE,
                                      exportselection=False)
        x = 1
        for index in self.route_handler.routes_df.index:
            list_string = f"{self.route_handler.routes_df['route_id'][index]}: {self.route_handler.routes_df['route_name'][index]} ({self.route_handler.routes_df['grade'][index]})"
            self.routes_listbox.insert(x, list_string)
            x += 1
        self.routes_listbox.grid_propagate(0)
        self.routes_listbox.grid(row=1, column=0, rowspan= 1, sticky='NESW')
        self.routes_listbox.bind("<<ListboxSelect>>", self.update_route)
        self.routes_listbox.bind("<Down>", self.OnEntryUpDown_routes_listbox)
        self.routes_listbox.bind("<Up>", self.OnEntryUpDown_routes_listbox)

        self.route_entry_frame.grid(row=row, column=column, rowspan=rowspan,
                                    columnspan=columnspan, sticky='NESW')

        self.routes_scrollbar = Scrollbar(self.route_entry_frame,
                                          orient='vertical')
        self.routes_scrollbar.config(command=self.routes_listbox.yview)
        self.routes_scrollbar.grid(row=1, column=1, rowspan=1, columnspan=1,
                                   sticky=(N,E,S,W))
        self.routes_listbox.config(yscrollcommand=self.routes_scrollbar.set)

    def create_grade_filter(self, row, column, rowspan, columnspan):

        self.grade_entry_frame = Frame(self.root, width = self.list_width,
                                       height = self.grades_height)
        self.grade_entry_frame.grid_propagate(0)
        self.grade_entry_frame.rowconfigure(1, weight=1)
        grade_entry_label = Label(self.grade_entry_frame, text="Select grades:")
        grade_entry_label.grid(row=0, column=0, rowspan=1, columnspan=1)
        self.grades = self.route_handler.get_grades()
        sorted_grades = self.sort_grade_list()

        self.grades_listbox = Listbox(self.grade_entry_frame,
                                      selectmode=MULTIPLE,
                                      exportselection=False)
        x = 1
        for grade in sorted_grades:
            self.grades_listbox.insert(x, grade)
            x += 1
        self.grades_listbox.grid(row=1, column=0, rowspan=1, columnspan=1,
                                 sticky=(N,E,S,W))
        self.grades_listbox.bind("<<ListboxSelect>>", self.update_routes_listbox)

        self.grade_entry_frame.grid(row=row, column=column, rowspan=rowspan,
                                    columnspan=columnspan, sticky='NESW')

        self.grades_scrollbar = Scrollbar(self.grade_entry_frame,
                                          orient='vertical')
        self.grades_scrollbar.config(command = self.grades_listbox.yview)
        self.grades_scrollbar.grid(row=1, column=1, rowspan=1, columnspan=1,
                                   sticky=('NESW'))
        self.grades_listbox.config(yscrollcommand=self.grades_scrollbar.set)

    def sort_grade_list(self):
        grade_order = ['3-','3','3+','4-','4','4+','5-','5','5+',
                       '6A','6A+','6B','6B+','6C','6C+',
                       '7A','7A+','7B','7B+','7C','7C+']
        count = 0
        while count < len(grade_order):
            if grade_order[count] not in self.grades:
                grade_order.remove(grade_order[count])
            else:
                count += 1
        for grade in self.grades:
            if grade not in grade_order:
                grade_order.append(grade)
        return grade_order

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
        route = self.route_handler.load_route(route_id)
        img = route_visualiser.show_route(route)

        img = self.convert_cv2_to_pil(img)

        resized_image = img.resize((int(self.img_width), int(self.img_height)))

        self.display_image_on_route_canvas(resized_image)

    def display_image_on_route_canvas(self, route_image):
        self.canvas.image = ImageTk.PhotoImage(route_image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def create_buttons(self, row, column, rowspan, columnspan):
        button_frame = Frame(self.root, width=self.list_width,
                             height=self.buttons_height)
        button_frame.grid_propagate(0)
        
        add_route_button = Button(button_frame, text="Add route",
                                  command=self.add_route)
        add_route_button.pack(side = LEFT, padx = self.list_width/20)
##        add_route_button.grid(row=2, column=1, rowspan=1, columnspan=1)

        quit_button = Button(button_frame, text='Quit',
                             command=self.root.destroy)
        quit_button.pack(side = RIGHT, padx = self.list_width/20)
##        quit_button.grid(row=2, column=1, rowspan=1, columnspan=1)

        button_frame.grid(row=row, column=column, rowspan=rowspan,
                          columnspan=columnspan, sticky='NESW')


if __name__ == "__main__":
    route_handler = RouteHandler()
    route_visualiser = RouteVisualiser()
    tk_app = TkApp(route_handler, route_visualiser)
    tk_app.root.mainloop()

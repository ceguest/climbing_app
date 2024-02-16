from tkinter import *
from route_handler import RouteHandler
from route_visualiser import RouteVisualiser
from PIL import Image as IM
from PIL import ImageTk
import cv2

NUMBERED_IMAGE = "static/Hold_Numbers_Markup.png"
BASE_IMAGE = "static/Board_Layout.png"

def get_base_image():
    img = IM.open(BASE_IMAGE)
    width, height = img.size
    img_res = img.resize((800, 600))
    return img


def convert_cv2_to_pil(img):
    # Rearrange the color channel
    b, g, r = cv2.split(img)
    img = cv2.merge((r, g, b))

    # Convert the cv2 Image object into a tk Image object
    im = IM.fromarray(img)
    return im


class TkApp:
    def __init__(self, route_handler, route_visualiser):
        self.canvas = None
        self.routes_listbox = None
        
        self.route_handler = route_handler
        self.route_visualiser = route_visualiser
        self.root = Tk()

        route_image = get_base_image()
        self.create_route_canvas(row=0, column=0, rowspan=50, columnspan=3)
        self.display_image_on_route_canvas(route_image)

        self.create_routes_listbox(row=0, column=3, rowspan=31, columnspan=1)

        self.create_grade_filter(row=31, column=3, rowspan=19, columnspan=1)

    def display_image_on_route_canvas(self, route_image):
        self.img_res = route_image.resize((800, 600))
        self.canvas.image = ImageTk.PhotoImage(self.img_res)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def create_route_canvas(self, row, column, rowspan, columnspan):
        self.canvas = Canvas(self.root, width=800, height=600)
        self.canvas.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)

    def update_routes_listbox(self, event=None):
        grade_indicies = self.grades_listbox.curselection()
        grades = []
        for index in grade_indicies:
            grades.append(self.grades_listbox.get(index))
        routes = self.route_handler.get_filtered_routes(grades=grades)
        self.routes_listbox.delete(0, END)
        x = 1
        for index in routes.index:
            list_string = f"{routes['route_id'][index]}: {routes['route_name'][index]} ({routes['grade'][index]})"
            self.routes_listbox.insert(x, list_string)
            x += 1

    def create_routes_listbox(self, row, column, rowspan, columnspan):
        route_entry_label = Label(self.root, text="Select route:")
        route_entry_label.grid(row=row, column=column, rowspan=1, columnspan=columnspan)
        
        self.routes_listbox = Listbox(self.root, selectmode=SINGLE, exportselection=False)
        x = 1
        for index in self.route_handler.routes_df.index:
            list_string = f"{self.route_handler.routes_df['route_id'][index]}: {self.route_handler.routes_df['route_name'][index]} ({self.route_handler.routes_df['grade'][index]})"
            self.routes_listbox.insert(x, list_string)
            x += 1
        self.routes_listbox.grid(row=row+1, column=column, rowspan=rowspan-1, sticky=(N, S, E, W))
        self.routes_listbox.bind("<<ListboxSelect>>", self.update_route)
        self.routes_listbox.bind("<Down>", self.OnEntryUpDown_routes_listbox)
        self.routes_listbox.bind("<Up>", self.OnEntryUpDown_routes_listbox)

    def create_grade_filter(self, row, column, rowspan, columnspan):
        grade_entry_label = Label(self.root, text="Select grades:")
        grade_entry_label.grid(row=row, column=column, rowspan=1, columnspan=columnspan)
        grades = self.route_handler.get_grades()

        self.grades_listbox = Listbox(self.root, selectmode=MULTIPLE, exportselection=False)
        x = 1
        for grade in grades:
            self.grades_listbox.insert(x, grade)
            x += 1
        self.grades_listbox.grid(row=row+1, column=column, rowspan=rowspan-1, sticky=(N, S, E, W))
        self.grades_listbox.bind("<<ListboxSelect>>", self.update_routes_listbox)

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
        if route_index == ():
            self.canvas.image = ImageTk.PhotoImage(self.img_res)
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
            return

        route_string = self.routes_listbox.get(route_index)
        route_id = int(route_string.split(":")[0])
        route = self.route_handler.load_route(route_id)
        img = route_visualiser.show_route(route)

        img = convert_cv2_to_pil(img)

        # width, height = img.size
        img_res = img.resize((800, 600))

        self.canvas.image = ImageTk.PhotoImage(img_res)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')


if __name__ == "__main__":
    route_handler = RouteHandler()
    route_visualiser = RouteVisualiser()
    tk_app = TkApp(route_handler, route_visualiser)
    tk_app.root.mainloop()

from tkinter import Button, Tk


class RouteMenu:
    def __init__(self, controller):
        self.route_menu = Tk()
        self.route_menu.title('Menu')
        self.route_menu.geometry('200x200')

        add_route_button = Button(self.route_menu, text="Add route",
                                  command=controller.add_route)
        add_route_button.pack(pady=20)

        edit_route_button = Button(self.route_menu, text="Edit route",
                                   command=controller.edit_route)
        edit_route_button.pack(pady=20)

    def close(self):
        self.route_menu.destroy()
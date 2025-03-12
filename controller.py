import image_utils
from view.main_view import View
from model.hold_handler import HoldHandler
from model.route import Route
from model.route_handler import RouteHandler
from route_visualiser import RouteVisualiser


class Controller:
    def __init__(self, route_handler: RouteHandler, hold_handler: HoldHandler, route_visualizer: RouteVisualiser):
        self.hold_handler = hold_handler
        self.route_handler = route_handler
        self.route_visualizer = route_visualizer
        self.view = View(self)
        self.currently_selected_route = None
        self.route_being_edited = None

    def update_current_route(self, route_id: int):
        route = self.route_handler.load_route(route_id)
        self.currently_selected_route = route
        self.update_displayed_route(route)

    def update_displayed_route(self, route: Route):
        route = self.route_handler.load_route(route.id)
        route_image = self.route_visualizer.show_route(route)
        img = image_utils.convert_cv2_to_pil(route_image)

        resized_image = img.resize((int(self.view.main_window.img_width), int(self.view.main_window.img_height)))
        self.view.canvas.display_image_on_route_canvas(resized_image)

    def get_route_strings(self) -> list[str]:
        return self.route_handler.list_route_strings()

    def apply_grade_filter(self, grades: list[str]) -> None:
        route_strings = self.route_handler.list_filtered_route_strings(grades=grades)
        self.view.routes_listbox.display_route_strings(route_strings)

    def get_grades(self) -> list[str]:
        return self.route_handler.list_grades()

    def filter_routes(self, grades: list[str]):
        routes = self.route_handler.get_filtered_routes(grades=grades)
        self.view.routes_listbox.update_routes_listbox(routes)

    def add_route(self):
        self.view.route_menu.close()
        self.route_being_edited = Route(name='New Route', specials={}, holds={}, comments='')

        route_image = self.route_visualizer.show_route(None, include_comments=False, include_all_holds=True)
        img = image_utils.convert_cv2_to_pil(route_image)

        resized_image = img.resize((int(self.view.main_window.img_width), int(self.view.main_window.img_height)))
        self.view.run_route_editor(resized_image)

    def edit_route(self):
        self.view.route_menu.close()
        route_image = self.route_visualizer.show_route(self.currently_selected_route, include_comments=False,
                                                       include_all_holds=True)
        img = image_utils.convert_cv2_to_pil(route_image)

        resized_image = img.resize((int(self.view.main_window.img_width), int(self.view.main_window.img_height)))
        self.view.run_route_editor(resized_image)

    def route_menu(self):
        self.view.run_route_menu()

    def canvas_click(self, x, y, key):
        print(f"Clicked at x: {x}, y: {y}, key: {key}")
        converted_x = int(x * 2.86)
        converted_y = int(y * 2.86) #why? TODO
        print(f"Converted x: {converted_x}, y: {converted_y}")

        self.add_hold(self.route_being_edited, converted_x, converted_y)
        route_image = self.route_visualizer.show_route(self.route_being_edited, include_comments=False, include_all_holds=True)
        img = image_utils.convert_cv2_to_pil(route_image)

        resized_image = img.resize((int(self.view.main_window.img_width), int(self.view.main_window.img_height)))
        self.view.editor_canvas.display_image_on_route_canvas(resized_image)

    def add_hold(self, route: Route, x, y):
        new_hold = self.hold_handler.get_nearby_hold(x, y)
        route.add_holds({new_hold.id: new_hold})


if __name__ == "__main__":
    hold_handler = HoldHandler()
    route_handler = RouteHandler(hold_handler)
    route_visualizer = RouteVisualiser()

    controller = Controller(route_handler, hold_handler, route_visualizer)
    controller.view.root.mainloop()

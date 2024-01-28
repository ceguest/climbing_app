from route_handler import RouteHandler
from route_visualiser import RouteVisualiser


if __name__ == '__main__':
    route_handler = RouteHandler()
    route_visualiser = RouteVisualiser()

    route_id = input("Enter route id: ")
    route = route_handler.load_route(route_id)

    route_visualiser.show_route(route)

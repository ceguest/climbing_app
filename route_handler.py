import pandas as pd
from route import Route
from hold_handler import HoldHandler
from foot_handler import FootHandler


class RouteHandler:
    def __init__(self):
        self.routes_df = None
        self.read_routes()

    def read_routes(self):
        self.routes_df = pd.read_csv('static/routes.csv', sep=";")

    def load_route(self, route_id):
        hold_handler = HoldHandler()
        foot_handler = FootHandler()
        df = self.routes_df
        route_data = df.loc[df['route_id'] == int(route_id)]

        try:
            hold_ids = route_data["holds"].values[0].split(",")
            holds = hold_handler.get_holds(hold_ids)
        except:
            holds = {}

        try:
            special_ids = route_data["specials"].values[0].split(",")
            specials = hold_handler.get_holds(special_ids)
        except:
            specials = {}

        try:
            feet_locs = route_data["feet"].values[0]
            feet = foot_handler.parse_feet(feet_locs)
        except:
            feet = []

        route = Route(
            id=route_data["route_id"].values[0],
            name=route_data["route_name"].values[0],
            specials=specials,
            holds=holds,
            grade=route_data["grade"].values[0],
            comments=route_data["comments"].values[0],
            feet=feet,
            date_set=route_data["date_set"].values[0],
            setter=route_data["setter"].values[0]
        )
        return route

    def get_route_ids(self):
        return self.routes_df["route_id"].values

    def get_grades(self):
        return set(self.routes_df["grade"].values)

    def get_filtered_routes(self, grades):
        if grades == []:
            return self.routes_df
        return self.routes_df[self.routes_df['grade'].isin(grades)]

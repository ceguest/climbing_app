import pandas as pd
from route import Route
from hold_handler import HoldHandler

class RouteHandler:
    def __init__(self):
        self.routes_df = self.read_routes()

    def read_routes(self):
        df = pd.read_csv('static/routes.csv', sep=";")
        return df

    def load_route(self, route_id):
        hold_handler = HoldHandler()
        df = self.routes_df
        route_data = df.loc[df['route_id'] == int(route_id)]
        hold_ids = route_data["holds"].values[0].split(",")

        holds = hold_handler.get_holds(hold_ids)
        route = Route(
            id=route_data["route_id"].values[0],
            name=route_data["route_name"].values[0],
            holds=holds,
            grade=route_data["grade"].values[0]
        )
        return route

    def get_route_ids(self):
        return self.routes_df["route_id"].values

    def get_grades(self):
        return set(self.routes_df["grade"].values)
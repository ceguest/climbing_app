from typing import List

import pandas as pd
from .route import Route
from hold_handler import HoldHandler


def _parse_feet(feet_locs):
    return eval(feet_locs)


def _sort_grade_list(grades: List[str]) -> List[str]:
    grade_order = ['3-', '3', '3+', '4-', '4', '4+', '5-', '5', '5+',
                   '6A', '6A+', '6B', '6B+', '6C', '6C+',
                   '7A', '7A+', '7B', '7B+', '7C', '7C+']
    count = 0
    while count < len(grade_order):
        if grade_order[count] not in grades:
            grade_order.remove(grade_order[count])
        else:
            count += 1
    for grade in grades:
        if grade not in grade_order:
            grade_order.append(grade)
    return grade_order


class RouteHandler:
    def __init__(self, hold_handler: HoldHandler):
        self.currently_selected_route = None
        self.routes_df = None
        self._read_routes()
        self.hold_handler = hold_handler

    def add_route(self, route: Route):
        df3 = pd.DataFrame(route.json(), index=[0])

        df3.to_csv('static/routes.csv', sep=';', mode='a', index=False, header=False)

    def update_route(self, route: Route):
        self.routes_df.iloc[route.id - 1] = route.json()

        self.routes_df.to_csv('static/routes.csv', sep=';', mode='w+', index=False, header=True)

    def load_route(self, route_id: int) -> Route:
        hold_handler = self.hold_handler
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
            feet = _parse_feet(feet_locs)
        except:
            feet = []

        route = Route(
            route_id=route_data["route_id"].values[0],
            name=route_data["route_name"].values[0],
            specials=specials,
            holds=holds,
            grade=route_data["grade"].values[0],
            comments=route_data["comments"].values[0],
            feet=feet,
            date_set=route_data["date_set"].values[0],
            setter=route_data["setter"].values[0]
        )
        self.currently_selected_route = route
        return route

    def get_current_route(self):
        return self.currently_selected_route

    def set_current_route(self, route: Route):
        self.currently_selected_route = route

    def _read_routes(self):
        self.routes_df = pd.read_csv('static/routes.csv', sep=";")

    def list_grades(self):
        return _sort_grade_list(set(self.routes_df["grade"].values))

    def get_filtered_routes(self, grades: List[str]):
        # if grades == []:
        if not grades:
            return self.routes_df
        return self.routes_df[self.routes_df['grade'].isin(grades)]

    def list_route_strings(self) -> list[str]:
        route_strings = []
        for index in self.routes_df.index:
            route_string = f"{self.routes_df['route_id'][index]}: {self.routes_df['route_name'][index]} ({self.routes_df['grade'][index]})"
            route_strings.append(route_string)
        return route_strings

    def list_filtered_route_strings(self, grades: List[str]) -> list[str]:
        route_strings = []
        for index in self.get_filtered_routes(grades).index:
            route_string = f"{self.routes_df['route_id'][index]}: {self.routes_df['route_name'][index]} ({self.routes_df['grade'][index]})"
            route_strings.append(route_string)
        return route_strings

    def check_route_already_exists(self, route: Route):
        new_route_all_holds = list(set(list(route.holds.keys()) + list(route.specials.keys())))
        new_route_all_holds.sort()

        for i in range(len(self.routes_df)):
            route_data = self.routes_df.iloc[i]
            # test = self.routes_df.loc[self.routes_df['route_id'] == int(i + 1)]
            try:
                route_specials = route_data['specials'].split(',')
                route_specials = [int(x) for x in route_specials]
            except:
                route_specials = []
            try:
                route_holds = route_data['holds'].split(',')
                route_holds = [int(x) for x in route_holds]
            except:
                route_holds = []
            route_all_holds = list(set(route_specials + route_holds))
            route_all_holds.sort()
            if route_all_holds == new_route_all_holds:
                route_nr = route_data['route_id']
                route_name = route_data['route_name']
                return True, route_nr, route_name
        return False, None, None

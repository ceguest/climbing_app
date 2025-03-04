import cv2
import pandas as pd

from hold_handler import HoldHandler
##from route_handler import RouteHandler
from datetime import datetime as dt
from tkinter import Toplevel
from tkinter import simpledialog as sd


class RouteAdder:
    def __init__(self):
        self.hold_handler = HoldHandler()
        self.base_img = self.create_base_img()
        self.route_holds = {}
        self.special_holds = {}
        self.foot_holds = []
        self.existing_route = None

    def load_existing_route(self, route):
        self.existing_route = route
        self.route_holds = route.holds_dict()
        self.special_holds = route.special_holds_dict()
        self.foot_holds = route.feet

    def create_base_img(self):
        img = cv2.imread('static/Board_Layout.png', 1)
        all_hold_ids = self.hold_handler.get_all_hold_ids()
        holds = self.hold_handler.get_holds(all_hold_ids)
        for hold_id in holds.values():
            cv2.circle(img, (hold_id.x_coord, hold_id.y_coord),
                       20, (0, 0, 255), -1)

        cv2.rectangle(img, (1300, 2400), (2700, 3000), (0, 0, 0), -1)

        return img

    def create_route(self):
        font = cv2.FONT_HERSHEY_COMPLEX

        close_window_message = "Press any key to close this window once all holds are selected."
        add_hold_message = "L-click to add a hold,"
        special_hold_message = "Ctrl + L-click to add a start/finish,"
        remove_hold_message = "Shift + L-click to remove any hand hold,"
        foot_hold_message = "R-click to add a foot hold,"
        remove_foot_hold_message = "Shift + R-click to remove a foot hold"

        cv2.putText(self.base_img, close_window_message, (100, 100), font, 2, (255, 255, 255), 5)
        cv2.putText(self.base_img, add_hold_message, (1400, 2500), font, 1.5, (255, 255, 255), 5)
        cv2.putText(self.base_img, special_hold_message, (1400, 2600), font, 1.5, (255, 255, 255), 5)
        cv2.putText(self.base_img, remove_hold_message, (1400, 2700), font, 1.5, (255, 255, 255), 5)
        cv2.putText(self.base_img, foot_hold_message, (1400, 2800), font, 1.5, (255, 255, 255), 5)
        cv2.putText(self.base_img, remove_foot_hold_message, (1400, 2900), font, 1.5, (255, 255, 255), 5)

        img = self.base_img.copy()
        self.render_route(img)

        cv2.imshow('image', img)
        cv2.setWindowProperty('image', cv2.WND_PROP_TOPMOST, 1)
        cv2.setMouseCallback('image', self.click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def click_event(self, event, x, y, flags, params):
        img = self.base_img.copy()
        routeHolds = self.route_holds
        specialHolds = self.special_holds

        if event == cv2.EVENT_LBUTTONDOWN and flags == 1:  # Left click only; add hold
            self.add_hold(routeHolds, specialHolds, x, y)

        elif event == cv2.EVENT_LBUTTONDOWN and flags == 17:  # Left click + shift; remove hold
            self.remove_hold(routeHolds, specialHolds, x, y)

        elif event == cv2.EVENT_RBUTTONDOWN and flags == 2:  # Right click; add foothold
            self.add_foothold(x, y)

        elif event == cv2.EVENT_RBUTTONDOWN and cv2.EVENT_FLAG_SHIFTKEY:  # Right click + shift; remove foothold
            self.remove_foothold(x, y)

        elif event == cv2.EVENT_LBUTTONDOWN and cv2.EVENT_FLAG_CTRLKEY:  # Left click + ctrl; remove hold
            self.add_special_hold(routeHolds, specialHolds, x, y)

        self.render_route(img)

        cv2.imshow('image', img)

    def render_route(self, img):
        for foot_hold in self.foot_holds:
            cv2.circle(img, (foot_hold[0], foot_hold[1]), 20, (128, 0, 128), 5)
        for hold_key, hold_coords in self.route_holds.items():
            cv2.circle(img, (hold_coords[0], hold_coords[1]), 20, (255, 0, 0), -1)
        for special_hold_key, special_hold_coords in self.special_holds.items():
            cv2.circle(img, (special_hold_coords[0], special_hold_coords[1]), 20, (0, 255, 0), -1)

    def add_hold(self, routeHolds, specialHolds, x, y):
        new_hold = self.hold_handler.get_nearby_hold(x, y)
        hold_id = new_hold['id'].values[0]
        hold_x = new_hold['x'].values[0]
        hold_y = new_hold['y'].values[0]
        if hold_id in specialHolds.keys():
            specialHolds.pop(hold_id)
        if hold_id not in routeHolds.keys():
            routeHolds[hold_id] = (hold_x, hold_y)

    def add_foothold(self, x, y):
        foot_coords = (x, y)
        self.foot_holds.append(foot_coords)

    def add_special_hold(self, routeHolds, specialHolds, x, y):
        new_hold = self.hold_handler.get_nearby_hold(x, y)
        hold_id = new_hold['id'].values[0]
        hold_x = new_hold['x'].values[0]
        hold_y = new_hold['y'].values[0]
        if hold_id in routeHolds.keys():
            routeHolds.pop(hold_id)
        if hold_id not in specialHolds.keys():
            specialHolds[hold_id] = (hold_x, hold_y)

    def remove_hold(self, routeHolds, specialHolds, x, y):
        new_hold = self.hold_handler.get_nearby_hold(x, y)
        hold_id = new_hold['id'].values[0]
        if hold_id in routeHolds.keys():
            routeHolds.pop(hold_id)

        elif hold_id in specialHolds.keys():
            specialHolds.pop(hold_id)

    def remove_foothold(self, x, y):
        radius = 60
        for i in range(len(self.foot_holds)):
            x_delta = abs(self.foot_holds[i][0] - x)
            y_delta = abs(self.foot_holds[i][1] - y)
            print(f"x_delta: {x_delta}, y_delta: {y_delta}")
            if x_delta < radius and y_delta < radius:
                self.foot_holds.pop(i)

    def check_route_exists(self):
        all_routes_df = pd.read_csv('static/routes.csv', sep=";")

        new_route_all_holds = list(set(list(self.route_holds.keys()) + list(self.special_holds.keys())))
        new_route_all_holds.sort()

        for i in range(len(all_routes_df)):
            route_data = all_routes_df.iloc[i]
            test = all_routes_df.loc[all_routes_df['route_id'] == int(i + 1)]
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

    def append_route(self):
        df2 = pd.read_csv('static/routes.csv', sep=';')
        lastRouteID = df2['route_id'].iat[-1]

        newRouteID = lastRouteID + 1

        routeName = sd.askstring(title="Route Name",
                                 prompt="Enter a name for the route:",
                                 initialvalue="Route " + str(newRouteID))
        if routeName is None:
            routeName = "Route " + str(newRouteID)
        else:
            routeName = routeName.title()

        comments = sd.askstring(title="Comments",
                                prompt="Enter any comments",
                                initialvalue="")
        if comments is None:
            comments = ""

        specials = self.string_holds(self.special_holds)
        holds = self.string_holds(self.route_holds)

        grade = sd.askstring(title="Grade",
                             prompt="Enter a grade for the route:",
                             initialvalue="TBC")
        if grade is None:
            grade = "TBC"
        else:
            grade = grade.upper()

        setter = sd.askstring(title="Setter",
                              prompt="Enter the route setter",
                              initialvalue="Unconfirmed")
        if setter is None:
            setter = "UNCONFIRMED"
        else:
            setter = setter.title()

        dateSet = dt.today().strftime('%d/%m/%Y')

        data = {'route_id': newRouteID,
                'route_name': routeName,
                'specials': specials,
                'holds': holds,
                'grade': grade,
                'setter': setter,
                'date_set': dateSet,
                'comments': comments,
                'feet': str(self.foot_holds)
                }

        df3 = pd.DataFrame(data, index=[0])

        df3.to_csv('static/routes.csv', sep=';', mode='a', index=False, header=False)

    def update_route(self):
        df2 = pd.read_csv('static/routes.csv', sep=';')

        routeID = self.existing_route.id

        newRouteName = sd.askstring(title="Route Name",
                                    prompt="Enter a name for the route:",
                                    initialvalue=self.existing_route.name)
        if newRouteName is None:
            routeName = self.existing_route.name
        else:
            routeName = newRouteName.title()

        comments = sd.askstring(title="Comments",
                                prompt="Enter any comments",
                                initialvalue=self.existing_route.comments)
        if comments is None:
            comments = self.existing_route.comments

        specials = self.string_holds(self.special_holds)
        holds = self.string_holds(self.route_holds)

        grade = sd.askstring(title="Grade",
                             prompt="Enter a grade for the route:",
                             initialvalue=self.existing_route.grade)
        if grade is None:
            grade = self.existing_route.grade
        else:
            grade = grade.upper()

        setter = sd.askstring(title="Setter",
                              prompt="Enter the route setter",
                              initialvalue=self.existing_route.setter)
        if setter is None:
            setter = self.existing_route.setter
        else:
            setter = setter.title()

        data = {
            'route_id': routeID,
            'route_name': routeName,
            'specials': specials,
            'holds': holds,
            'grade': grade,
            'setter': setter,
            'date_set': self.existing_route.date_set,
            'comments': comments,
            'feet': str(self.foot_holds)
        }

        df2.iloc[routeID - 1] = data

        df2.to_csv('static/routes.csv', sep=';', mode='w+', index=False, header=True)

    def string_holds(self, holdList):
        holds1 = []
        for i in holdList:
            holds1.append(str(i))
        holds2 = ', '.join(holds1)
        return holds2

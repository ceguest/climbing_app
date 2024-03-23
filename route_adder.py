import cv2
import pandas as pd

from hold_handler import HoldHandler
##from route_handler import RouteHandler
from datetime import datetime as dt
from tkinter import Toplevel
from tkinter import simpledialog as sd
from math import isnan


class RouteAdder:
    def __init__(self):
        self.hold_handler = HoldHandler()
        self.base_img = self.create_base_img()
        self.route_holds = []
        self.special_holds = []

    def create_base_img(self):
        img = cv2.imread('static/Board_Layout.png', 1)
        all_hold_ids = self.hold_handler.get_all_hold_ids()
        holds = self.hold_handler.get_holds(all_hold_ids)
        for hold_id in holds.values():
            cv2.circle(img, (hold_id.x_coord, hold_id.y_coord),
                       20, (0, 0, 255), -1)

        return img

    def create_route(self):
        font = cv2.FONT_HERSHEY_COMPLEX

        close_window_message = "Press any key to close this window once all holds are selected."
        add_hold_message = "L-click to add a hold,"
        special_hold_message = "Shift + L-click to add a start/finish,"
        remove_hold_message = "R-click to remove any hold."

        cv2.putText(self.base_img, close_window_message, (100, 100), font, 2, (255, 255, 255), 5)
        cv2.putText(self.base_img, add_hold_message, (1400, 2700), font, 1.5, (255, 255, 255), 5)
        cv2.putText(self.base_img, special_hold_message, (1400, 2800), font, 1.5, (255, 255, 255), 5)
        cv2.putText(self.base_img, remove_hold_message, (1400, 2900), font, 1.5, (255, 255, 255), 5)
        cv2.imshow('image', self.base_img)
        cv2.setWindowProperty('image', cv2.WND_PROP_TOPMOST, 1)
        cv2.setMouseCallback('image', self.click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def click_event(self, event, x, y, flags, params):
        img = self.base_img
        routeHolds = self.route_holds
        specialHolds = self.special_holds

        if event == cv2.EVENT_LBUTTONDOWN and flags == 1:

            new_hold = self.hold_handler.get_nearby_hold(x, y)
            hold_id = new_hold['id'].values[0]
            hold_x = new_hold['x'].values[0]
            hold_y = new_hold['y'].values[0]

            if hold_id in specialHolds:
                specialHolds.remove(hold_id)

            if hold_id not in routeHolds:
                routeHolds.append(hold_id)

                cv2.circle(img, (hold_x, hold_y),
                           20, (255, 0, 0), -1)

                cv2.imshow('image', img)

        elif event == cv2.EVENT_LBUTTONDOWN and flags == 17:

            new_hold = self.hold_handler.get_nearby_hold(x, y)
            hold_id = new_hold['id'].values[0]
            hold_x = new_hold['x'].values[0]
            hold_y = new_hold['y'].values[0]

            if hold_id in routeHolds:
                routeHolds.remove(hold_id)

            if hold_id not in specialHolds:
                specialHolds.append(hold_id)

                cv2.circle(img, (hold_x, hold_y),
                           20, (0, 255, 0), -1)

                cv2.imshow('image', img)

        elif event == cv2.EVENT_RBUTTONDOWN:

            new_hold = self.hold_handler.get_nearby_hold(x, y)
            hold_id = new_hold['id'].values[0]
            hold_x = new_hold['x'].values[0]
            hold_y = new_hold['y'].values[0]

            if hold_id in routeHolds:
                routeHolds.remove(hold_id)

                cv2.circle(img, (hold_x, hold_y),
                           20, (0, 0, 255), -1)

                cv2.imshow('image', img)

            elif hold_id in specialHolds:
                specialHolds.remove(hold_id)

                cv2.circle(img, (hold_x, hold_y),
                           20, (0, 0, 255), -1)

                cv2.imshow('image', img)

    def check_route_exists(self):
        all_routes_df = pd.read_csv('static/routes.csv', sep=";")
        
        new_route_all_holds = list(set(self.route_holds + self.special_holds))
        new_route_all_holds.sort()
        
        for i in range(len(all_routes_df)):
            route_data = all_routes_df.iloc[i]
            test = all_routes_df.loc[all_routes_df['route_id']==int(i+1)]
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
        else:routeName = routeName.title()
            

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
                'date_set': dateSet
                }

        df3 = pd.DataFrame(data, index=[0])

        df3.to_csv('static/routes.csv', sep=';', mode='a', index=False, header=False)

    def string_holds(self, holdList):
        holds1 = []
        for i in holdList:
            holds1.append(str(i))
        holds2 = ', '.join(holds1)
        return holds2

import cv2
import pandas as pd

from hold_handler import HoldHandler
from datetime import datetime as dt

class RouteAdder:
    def __init__(self):
        self.hold_handler = HoldHandler()
        self.base_img = cv2.imread('static/Basic_Layout.jpeg', 1)
        self.route_holds = []
        self.special_holds = []



    def create_route(self):
        font = cv2.FONT_HERSHEY_COMPLEX

        cv2.putText(self.base_img,
                    "Press any key to close this window once all holds are selected",
                    (100, 100), font, 2, (255, 255, 255), 5)
        cv2.imshow('image', self.base_img)
        cv2.setMouseCallback('image', self.click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def click_event(self, event, x, y, flags, params):
        df = self.hold_handler.holds_df
        img = self.base_img
        routeHolds = self.route_holds
        specialHolds = self.special_holds

        if event == cv2.EVENT_LBUTTONDOWN and flags == 1:

            new_hold = self.hold_handler.get_nearby_hold(x, y)
            hold_id = new_hold['id'].values[0]
            hold_x = new_hold['x'].values[0]
            hold_y = new_hold['y'].values[0]
            # hold_used = [hold_id]
            # hold_coord = get_coord_list('Coord_List.txt', hold_used)

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

    def append_route(self):
        df2 = pd.read_csv('static/routes.csv', sep=';')
        lastRouteID = df2['route_id'].iat[-1]

        newRouteID = lastRouteID + 1
        routeName = "Route " + str(newRouteID)
        specials = self.string_holds(self.special_holds)
        holds = self.string_holds(self.route_holds)
        grade = "TBC"
        setter = "UNCONFIRMED"
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
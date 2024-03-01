# Take hold coordinates based on numbered list and mark on image

import cv2

class RouteVisualiser:
    def __init__(self):
        self.base_image_name = "static/Board_Layout.jpeg"

    def show_route(self, route):
        font = cv2.FONT_HERSHEY_COMPLEX

        img = cv2.imread(self.base_image_name)
        cv2.putText(img, f"{route.id}: {route.name} ({route.grade})",
                    (1300, 2900), font, 2, (255, 255, 255), 5)
        for hold_id in route.holds:
            hold = route.holds[hold_id]
            cv2.circle(img, (hold.x_coord, hold.y_coord), 20, (255, 255, 0), -1)
        for hold_id in route.specials:
            hold = route.specials[hold_id]
            cv2.circle(img, (hold.x_coord, hold.y_coord), 20, (0, 0, 255), -1)
        return img


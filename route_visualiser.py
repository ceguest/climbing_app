# Take hold coordinates based on numbered list and mark on image

import cv2
import textwrap

from model.hold_handler import HoldHandler


class RouteVisualiser:
    def __init__(self):
        self.base_image_name = "static/Board_Layout.jpeg"

    def show_route(self, route, include_comments=False, include_all_holds=False):
        img = cv2.imread(self.base_image_name)

        if include_comments:
            comments = route.comments
            wrapped_comments = textwrap.fill(comments, 47)
            wrapped_comments = wrapped_comments.split("\n")

            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.rectangle(img, (1100, 2400), (2900, 3000), (0, 0, 0), -1)

            cv2.putText(img, f"{route.id}: {route.name} ({route.grade})",
                        (1150, 2500), font, 2, (255, 255, 255), 5)

            line_position = 2620
            for comment_line in wrapped_comments:
                cv2.putText(img, comment_line,
                            (1150, line_position), font, 2, (255, 255, 255), 5)
                line_position += 100

        if include_all_holds:
            hold_handler = HoldHandler()
            all_hold_ids = hold_handler.get_all_hold_ids()
            holds = hold_handler.get_holds(all_hold_ids)
            for hold_id in holds.values():
                cv2.circle(img, (hold_id.x_coord, hold_id.y_coord), 20, (0, 0, 255), -1)

        if route:
            for hold_id in route.holds:
                hold = route.holds[hold_id]
                cv2.circle(img, (hold.x_coord, hold.y_coord), 20, (255, 255, 0), -1)
            for hold_id in route.specials:
                hold = route.specials[hold_id]
                cv2.circle(img, (hold.x_coord, hold.y_coord), 20, (0, 0, 255), -1)
            if route.feet:
                for foot in route.feet:
                    cv2.circle(img, (foot[0], foot[1]), 20, (128, 0, 128), 5)

        return img

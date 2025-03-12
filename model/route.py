from typing import Dict, List

import numpy as np


class Route:
    def __init__(
            self,
            name: str,
            specials: dict[str, (int, int)],
            holds: dict[str, (int, int)],
            comments: str,
            feet: list[(int, int)] = None,
            route_id: int = None,
            grade: str = None,
            date_set: str = None,
            setter: str = None
    ):
        self.id = route_id
        self.name = name
        self.specials = specials
        self.holds = holds
        self.feet = feet
        self.grade = grade
        if type(comments) == str:
            self.comments = comments
        else:
            self.comments = ''
        self.setter = setter
        self.date_set = date_set

    def add_holds(self, holds: dict[str, (int, int)]):
        self.holds.update(holds)
        for hold_id, hold in list(holds.items()):
            self.specials.pop(hold_id, None)

    def add_specials(self, specials: dict[str, (int, int)]):
        self.specials.update(specials)
        for hold_id, hold in list(specials.items()):
            self.holds.pop(hold_id, None)

    def remove_hold(self, hold_id: str):
        self.holds.pop(hold_id, None)
        self.specials.pop(hold_id, None)

    def remove_foothold(self, x, y):
        radius = 60
        for i in range(len(self.feet)):
            x_delta = abs(self.feet[i][0] - x)
            y_delta = abs(self.feet[i][1] - y)
            print(f"x_delta: {x_delta}, y_delta: {y_delta}")
            if x_delta < radius and y_delta < radius:
                self.feet.pop(i)

    def holds_dict(self):
        holds_dict = {}
        for hold_id, hold in list(self.holds.items()):
            holds_dict[np.int64(hold_id)] = (hold.x_coord, hold.y_coord)
        return holds_dict

    def special_holds_dict(self):
        holds_dict = {}
        for hold_id, hold in list(self.specials.items()):
            holds_dict[np.int64(hold_id)] = (hold.x_coord, hold.y_coord)
        return holds_dict

    def json(self):
        pass

import numpy as np
class Route:
    def __init__(self, name, specials, holds, comments, feet=None, id=None, grade=None, date_set=None, setter=None):
    def __init__(self, name, specials, holds, comments, feet=None, id=None, grade=None):
        self.id = id
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

    def holds_dict(self):
        dict = {}
        for hold_id, hold in list(self.holds.items()):
            dict[np.int64(hold_id)] = (hold.x_coord, hold.y_coord)
        return dict

    def special_holds_dict(self):
        dict = {}
        for hold_id, hold in list(self.specials.items()):
            dict[np.int64(hold_id)] = (hold.x_coord, hold.y_coord)
        return dict

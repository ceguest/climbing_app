class Route:
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

# date created
# setter
# notes

class FootHandler:
    # def __init__(self, feet):
    #     self.feet = feet

    def parse_feet(self, feet_locs):
        return eval(feet_locs)


if __name__ == "__main__":
    pass
    foot_handler = FootHandler()
    result = foot_handler.parse_feet("[(1,2)]")
    print(result[0])
    print(result[0][0])


# l click - add hold
# l click + shift - remove hold
# r click - add foothold
# r click + shift - remove foothold
# ctrl + l click - add special hold
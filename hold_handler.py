from hold import Hold
import pandas as pd


class HoldHandler:
    def __init__(self):
        self.holds_df = self.read_holds()

    def read_holds(self):
        df = pd.read_csv('static/Coord_List.txt')
        return df

    def get_holds(self, hold_ids):
        holds = {}
        df = self.holds_df
        for hold_id in hold_ids:
            hold_data = df.loc[df['id'] == int(hold_id)]
            holds[hold_id] = Hold(hold_data["x"].values[0], hold_data["y"].values[0], hold_data["id"].values[0])

        return holds

    def get_nearby_hold(self, x, y):
        radius = 20
        df = self.holds_df
        filtered_holds = df[(df['x'] < x + radius) &
                            (df['x'] > x - radius) &
                            (df['y'] < y + radius) &
                            (df['y'] > y - radius)]

        return filtered_holds
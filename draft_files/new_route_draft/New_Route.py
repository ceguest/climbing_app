import pandas as pd
import cv2, csv
from datetime import datetime as dt


def get_holds(filename):
    df = pd.read_csv(filename, sep=",")
    return df


def filter_holds(df, x, y):
    r = 20
    filter_df = df[(df['x'] < x + r) &
                   (df['x'] > x - r) &
                   (df['y'] < y + r) &
                   (df['y'] > y - r)]
    return filter_df


def get_hold_ID(df):
    holdID = df['id'].values[0]
    return holdID


def get_coord_list(hold_list, holds_used):
    # This is a duplicate of the code in Mark_Holds.py,
    # reused to avoid image overwrite when importing the .py file

    data_dict = {}
    coord_list = []

    with open(hold_list) as f:
        reader = csv.reader(f)
        data = list(reader)

    for i in data[1:]:
        data_dict[int(i[0])] = [int(i[1]), int(i[2])]

    for i in holds_used:
        coord_list.append(data_dict[i])

    return coord_list


def click_event(event, x, y, flags, params):
    global img, routeHolds, specialHolds, df

    if event == cv2.EVENT_LBUTTONDOWN and flags == 1:

        newHold = filter_holds(df, x, y)
        holdID = get_hold_ID(newHold)
        holdUsed = [holdID]
        holdCoord = get_coord_list('Coord_List.txt', holdUsed)

        if holdID in specialHolds:
            specialHolds.remove(holdID)

        if holdID not in routeHolds:
            routeHolds.append(holdID)

            cv2.circle(img, (holdCoord[0][0], holdCoord[0][1]),
                       20, (255, 0, 0), -1)

            cv2.imshow('image', img)

    elif event == cv2.EVENT_LBUTTONDOWN and flags == 17:

        newHold = filter_holds(df, x, y)
        holdID = get_hold_ID(newHold)
        holdUsed = [holdID]
        holdCoord = get_coord_list('Coord_List.txt', holdUsed)

        if holdID in routeHolds:
            routeHolds.remove(holdID)

        if holdID not in specialHolds:
            specialHolds.append(holdID)

            cv2.circle(img, (holdCoord[0][0], holdCoord[0][1]),
                       20, (0, 255, 0), -1)

            cv2.imshow('image', img)

    elif event == cv2.EVENT_RBUTTONDOWN:

        newHold = filter_holds(df, x, y)
        holdID = get_hold_ID(newHold)
        holdUsed = [holdID]
        holdCoord = get_coord_list('Coord_List.txt', holdUsed)

        if holdID in routeHolds:
            routeHolds.remove(holdID)

            cv2.circle(img, (holdCoord[0][0], holdCoord[0][1]),
                       20, (0, 0, 255), -1)

            cv2.imshow('image', img)

        elif holdID in specialHolds:
            specialHolds.remove(holdID)

            cv2.circle(img, (holdCoord[0][0], holdCoord[0][1]),
                       20, (0, 0, 255), -1)

            cv2.imshow('image', img)


def create_route():
    global img, routeHolds

    font = cv2.FONT_HERSHEY_COMPLEX

    cv2.putText(img,
                "Press any key to close this window once all holds are selected",
                (100, 100), font, 2, (255, 255, 255), 5)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return routeHolds, specialHolds


def string_holds(holdList):
    holds1 = []
    for i in holdList:
        holds1.append(str(i))
    holds2 = ', '.join(holds1)
    return holds2


def append_route(routeHolds, specialHolds):
    df2 = pd.read_csv('routes.csv', sep=';')
    lastRouteID = df2['route_id'].iat[-1]

    newRouteID = lastRouteID + 1
    routeName = "Route " + str(newRouteID)
    specials = string_holds(specialHolds)
    holds = string_holds(routeHolds)
    grade = "TBC"
    setter = "Tom"
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

    df3.to_csv('routes.csv', sep=';', mode='a', index=False, header=False)


if __name__ == "__main__":
    df = get_holds('Coord_List.txt')

    img = cv2.imread('Basic_Layout.jpeg', 1)
    routeHolds = []
    specialHolds = []

    routeHolds, specialHolds = create_route()

    append_route(routeHolds, specialHolds)

# Take hold coordinates based on numbered list and mark on image

import cv2, csv

def get_coord_list(hold_list, holds_used):

    data_dict = {}
    coord_list = []

    with open(hold_list) as f:
        reader = csv.reader(f)
        data = list(reader)

    for i in data:
        data_dict[int(i[0])]=[int(i[1]),int(i[2])]

    for i in holds_used:
        coord_list.append(data_dict[i])

    return coord_list

def mark_holds(img_name, coord_list):

    font = cv2.FONT_HERSHEY_COMPLEX

    img = cv2.imread(img_name)
    cv2.putText(img, "Press any key to close this window", (100,100), font, 2, (255,255,255), 5)
    for i in coord_list:
        cv2.circle(img, (i[0],i[1]), 20, (0,0,255), -1)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


img_name = "Board_Layout.jpeg"
holds_used = [6,16,37,63,81]
hold_list = "Coord_List.txt"
coord_list = get_coord_list(hold_list, holds_used)

mark_holds(img_name,coord_list)

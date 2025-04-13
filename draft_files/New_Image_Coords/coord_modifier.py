import cv2, math

old_img = cv2.imread('Hold_Numbers_Markup.jpeg',1)
new_img = cv2.imread('New_Board_Layout.jpeg',1)

old_limits = []
new_limits = []

n = 0

def click_event_1(event, x, y, flags, params):

    global old_img, n , old_limits

    if event == cv2.EVENT_LBUTTONDOWN:

        coord = [n, x, y]
        old_limits.append(coord)

        n += 1

def click_event_2(event, x, y, flags, params):

    global new_img, n , new_limits

    if event == cv2.EVENT_LBUTTONDOWN:

        coord = [n, x, y]
        new_limits.append(coord)

        n += 1


def compare_images():

    global n, old_img, old_limits, new_img, new_limits

    n = 1

    cv2.imshow('image', old_img)
    cv2.setMouseCallback('image', click_event_1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    with open("Old_Coord_List.txt","w") as filename:
        for i in old_limits:
            j = str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "\n"
            filename.write(j)

    n = 1

    cv2.imshow('image', new_img)
    cv2.setMouseCallback('image', click_event_2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    with open("New_Coord_List.txt","w") as filename:
        for i in new_limits:
            j = str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "\n"
            filename.write(j)


def find_img_centres():

    global old_limits, new_limits

    old_x = 0
    old_y = 0
    new_x = 0
    new_y = 0

    for i in old_limits:
        old_x += i[1]
        old_y += i[2]

    old_x = old_x / 4
    old_y = old_y / 4

    for i in new_limits:
        new_x += i[1]
        new_y += i[2]

    new_x = new_x / 4
    new_y = new_y / 4

    return (old_x,old_y) , (new_x,new_y)


def find_angle(centre, coord):

    angle = math.degrees(math.atan2(coord[1] - centre[1], coord[0] - centre[0]))

    if angle < 0:
        angle += 360

    return angle

def define_quadrants(old_centre):

    global old_limits

    quadrants = []

    for i in old_limits:
        angle = find_angle(old_centre, (i[1], i[2]))
        quadrants.append(angle)

    return quadrants

def find_quadrant(quadrants, centre, coord):

    angle = find_angle(old_centre, coord)
    
    if angle > quadrants[0] and angle < quadrants[1]:
        return 0
    elif angle > quadrants[1] and angle < 360 or angle > 0 and angle < quadrants[2]:
        return 1
    elif angle > quadrants[2] and angle < quadrants[3]:
        return 2
    else:
        return 3

def find_line_eqn(point1, point2):

    gradient = (point1[1] - point2[1]) / (point1[0] - point2[0])

    intercept = point1[1] - (gradient * point1[0])

    return gradient, intercept

def find_intersect(eqn1, eqn2):

    x = (eqn2[1] - eqn1[1]) / (eqn1[0] - eqn2[0])
    y = eqn1[0] * x + eqn1[1]

    return x, y

def find_ratio(end_coord1, end_coord2, mid_coord):

    len_main = ((end_coord1[0] - end_coord2[0])**2 +
                (end_coord1[1] - end_coord2[1])**2) ** 0.5

    len_part = ((end_coord1[0] - mid_coord[0])**2 +
                (end_coord1[1] - mid_coord[1])**2) ** 0.5

    ratio = len_part / len_main

    return ratio

def find_new_coord(end_coord1, end_coord2, ratio):

    dx = (end_coord2[0] - end_coord1[0]) * ratio
    dy = (end_coord2[1] - end_coord1[1]) * ratio

    x = end_coord1[0] + dx
    y = end_coord1[1] + dy

    return x, y


#def adjust_coordinates():
    # with open coord_list ...
    # for coord in coord_list
        # find quadrant
        # find eqns for each line
        # find intersection

def test_quadrants():

    test77 = (1557,401)
    test37 = (2613,1283)
    test3 = (2027,1791)
    test8 = (1205,1605)

    quadrant77 = find_quadrant(quadrants, old_centre, test77)
    print('hold 77 is in quadrant ',quadrant77)
    quadrant37 = find_quadrant(quadrants, old_centre, test37)
    print('hold 37 is in quadrant ',quadrant37)
    quadrant3 = find_quadrant(quadrants, old_centre, test3)
    print('hold 3 is in quadrant ',quadrant3)
    quadrant8 = find_quadrant(quadrants, old_centre, test8)
    print('hold 8 is in quadrant ',quadrant8)

def test_coord():

    global old_limits

    test77 = (1557,401)
    quad77 = find_quadrant(quadrants, old_centre, test77)
    eqn77 = find_line_eqn(test77, old_centre)

    i = quad77 + 1
    if i > 3:
        i -= 4

    old_perim_start = (old_limits[quad77][1],old_limits[quad77][2])
    old_perim_end = (old_limits[i][1],old_limits[i][2])

    new_perim_start = (new_limits[quad77][1],new_limits[quad77][2])
    new_perim_end = (new_limits[i][1],new_limits[i][2])

    eqn2 = find_line_eqn(old_perim_start,old_perim_end)

    x, y = find_intersect(eqn77, eqn2)

    ratio1 = find_ratio(old_perim_start, old_perim_end, (x,y))
    
    ratio2 = find_ratio((x,y), old_centre, test77)

    x1, y1 = find_new_coord(new_perim_start,new_perim_end, ratio1)

    x2, y2 = find_new_coord((x1,y1), new_centre, ratio2)

    return x2, y2


compare_images()
old_centre, new_centre = find_img_centres()
quadrants = define_quadrants(old_centre)
new_x, new_y = test_coord()







def mark_holds(x, y):

    font = cv2.FONT_HERSHEY_COMPLEX

    img = cv2.imread("New_Board_Layout.jpeg")
    cv2.putText(img, "Press any key to close this window", (100,100), font, 2, (255,255,255), 5)
    cv2.circle(img, (int(x), int(y)), 20, (0,0,255), -1)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

mark_holds(new_x, new_y)

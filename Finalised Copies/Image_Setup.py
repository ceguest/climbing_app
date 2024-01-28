# Set up base image:
# 1 - Extract coordinates for holds
# 2 - Print numbers onto holds

import cv2

img = cv2.imread('Board_Layout.jpeg',1)
n = 1
coord_list = []

def click_event(event, x, y, flags, params):

    global img, n, coord_list

    if event == cv2.EVENT_LBUTTONDOWN:

        if n < 10:
            tx = x-6
            ty = y+5
        else:
            tx = x-12
            ty = y+5
        
        new_coord = [n, x, y]
        coord_list.append(new_coord)

        cv2.circle(img, (x, y), 15, (255,0,0),-1)
        
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        cv2.putText(img, str(n), (tx,ty), font, 1, (255,255,255), 1)
        cv2.imshow('image', img)

        n += 1

def setup_base_image():
    global img, coord_list
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.imwrite('Hold_Numbers_Markup.jpeg',img)
    cv2.destroyAllWindows()
    with open("Coord_List.txt","w") as filename:
        for i in coord_list:
            j = str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "\n"
            filename.write(j)

#setup_base_image()

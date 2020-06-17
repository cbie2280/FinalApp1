import cv2
import dlib
import numpy as np



def shape_to_np(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)
    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    # return the list of (x, y)-coordinates
    return coords


def eye_on_mask(mask, side):
    points = [shape[i] for i in side]
    points = np.array(points, dtype=np.int32)
    mask = cv2.fillConvexPoly(mask, points, 255)
    return mask


def contouring(thresh, mid, img, right=False):
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    try:
        cnt = max(cnts, key=cv2.contourArea)
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        # print(cx,cy)
        if right:
            cx += mid
        # cv2.circle(img, (cx, cy), 4, (0, 0, 255), 2)
        cv2.circle(img, (cx, cy), 8, ([17, 15, 100]), 1)
        return (cx,cy)
    except:
        pass


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('C:\\Users\\Bianca\\PycharmProjects\\shape.dat')

left = [36, 37, 38, 39, 40, 41]
right = [42, 43, 44, 45, 46, 47]

cap = cv2.VideoCapture('C:\\Users\\Bianca\\PycharmProjects\\FinalApp\\static\\video.avi')
# cap = cv2.VideoCapture('C:\\Users\\Bianca\\Desktop\\videos\\hai.avi')
# cap = cv2.VideoCapture(0)
_, img = cap.read()
thresh = img.copy()

kernel = np.ones((9, 9), np.uint8)


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def mid1(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)


def nothing(x):
    pass


# cv2.createTrackbar('threshold', 'image', 0, 255, nothing)

xo=[0]
yo=[0]
i=0
while (True):
    _, img = cap.read()
    i=i+1
    if np.shape(img) != ():
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = detector(gray)
        for rect in rects:
            shape = predictor(gray, rect)
            shape = shape_to_np(shape)
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            mask = eye_on_mask(mask, left)
            mask = eye_on_mask(mask, right)
            mask = cv2.dilate(mask, kernel, 5)
            eyes = cv2.bitwise_and(img, img, mask=mask)
            mask = (eyes == [0, 0, 0]).all(axis=2)
            eyes[mask] = [255, 255, 255]
            mid = (shape[42][0] + shape[39][0]) // 2
            eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(eyes_gray, 80, 255, cv2.THRESH_BINARY)
            thresh = cv2.erode(thresh, None, iterations=2)  # 1
            thresh = cv2.dilate(thresh, None, iterations=4)  # 2
            thresh = cv2.medianBlur(thresh, 3)  # 3
            thresh = cv2.bitwise_not(thresh)

            bla=contouring(thresh[:, 0:mid], mid, img)
            bla1=contouring(thresh[:, mid:], mid, img, True)

            landmarks = predictor(gray, rect)
            left_point = (landmarks.part(36).x, landmarks.part(36).y)
            right_point = (landmarks.part(39).x, landmarks.part(39).y)
            center_top = mid1(landmarks.part(37), landmarks.part(38))
            center_bottom = mid1(landmarks.part(41), landmarks.part(40))


            left_point_r = (landmarks.part(42).x, landmarks.part(42).y)
            right_point_r = (landmarks.part(45).x, landmarks.part(45).y)
            center_top_r = mid1(landmarks.part(43), landmarks.part(44))
            center_bottom_r = mid1(landmarks.part(47), landmarks.part(46))


            a= int((left_point[0] + right_point[0])/2)
            b= int((left_point[1] + right_point[1])/2)
            centre=(a,b)

            c= int((left_point_r[0] + right_point_r[0])/2)
            d= int((left_point_r[1] + right_point_r[1])/2)
            centre_r=(c,d)


            if bla != None and bla1 != None:
                xdiff = (a - bla[0], c - bla1[0])
                ydiff = (b - bla[1], d - bla1[1])


                div = det(xdiff, ydiff)
                if div != 0:


                    line1 = ((a,b), bla)
                    line2 = ((c,d), bla1)

                    d = (det(*line1), det(*line2))
                    x = det(d, xdiff) / div
                    y = det(d, ydiff) / div

                    inter=(int(x),int(y))
                    print(inter)
                    xo.append(inter[0])
                    yo.append(inter[1])



                    # cv2.circle(img, (a, b), 8, ([255, 0, 0]), 1)
                    hor_line = cv2.line(img, left_point, right_point, (0, 255, 0), 1)
                    ver_line = cv2.line(img, center_top, center_bottom, (0, 255, 0), 1)
                    ver_line = cv2.line(img, bla, inter, (0, 0, 255), 2)

                    hor_line_r = cv2.line(img, left_point_r, right_point_r, (0, 255, 0), 1)
                    ver_line_r = cv2.line(img, center_top_r, center_bottom_r, (0, 255, 0), 1)
                    ver_line_r = cv2.line(img, bla1, inter, (0, 0, 255), 2)

                else:
                    xo.append(xo[len(xo) - 1])
                    yo.append(yo[len(yo) - 1])

            print(xo)
            print(len(xo))
            print(yo)
            print(len(yo))



        cv2.imshow('eyes', img)
        # cv2.imshow("image", thresh)



        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break
cap.release()
cv2.destroyAllWindows()


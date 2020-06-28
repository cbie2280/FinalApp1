import os
import cv2
import dlib
import numpy as np
from datetime import date
from random import shuffle

import sklearn
from flask import render_template, request, Response, jsonify
from flask import current_app
from flask_login import current_user
import pickle
from model.Result import Result
from utils.VideoCamera import VideoCamera
from utils.extensions import db

video_camera = None
global_frame = None


class CameraController:
    def __init__(self):
        pass



    def start(self):
        APP_ROOT = os.path.join('static', 'animals')
        APP_ROOT6 = os.path.join('static', 'js')
        current_app.config['UPLOAD_FOLDER'] = APP_ROOT
        current_app.config['UPLOAD_FOLDER2'] = APP_ROOT6
        dog = os.path.join(current_app.config['UPLOAD_FOLDER'], 'dog2.gif')
        cat = os.path.join(current_app.config['UPLOAD_FOLDER'], 'cat.gif')
        sound = os.path.join(current_app.config['UPLOAD_FOLDER'], 'mare.mp3')
        frog = os.path.join(current_app.config['UPLOAD_FOLDER'], 'frog.gif')
        chicken = os.path.join(current_app.config['UPLOAD_FOLDER'], 'chicken.gif')
        horse = os.path.join(current_app.config['UPLOAD_FOLDER'], 'horse.gif')
        video = os.path.join(current_app.config['UPLOAD_FOLDER2'], 'r3.js')

        dogS = os.path.join(current_app.config['UPLOAD_FOLDER'], 'dogS.mp3')
        catS = os.path.join(current_app.config['UPLOAD_FOLDER'], 'catS.mp3')
        frogS = os.path.join(current_app.config['UPLOAD_FOLDER'], 'frog.wav')
        chickenS = os.path.join(current_app.config['UPLOAD_FOLDER'], 'chicken.mp3')
        horseS = os.path.join(current_app.config['UPLOAD_FOLDER'], 'horse.wav')

        list = []
        list.append([dog, dogS])
        list.append([cat, catS])
        list.append([frog, frogS])
        list.append([chicken, chickenS])
        list.append([horse, horseS])
        shuffle(list)
        result = list[:3]

        return render_template('game.html', dog_image=dog, cat_image=cat, sound=sound, filename=video,
                               frog_image=frog, chicken_image=chicken, rabbit_image=horse, multe=result)

    def record_status(self):
        global video_camera
        if video_camera == None:
            video_camera = VideoCamera()

        json = request.get_json()

        status = json['status']

        if status == "true":
            video_camera.start_record()
            return jsonify(result="started")
        else:
            video_camera.stop_record()
            return jsonify(result="stopped")

    def video_stream(self):
        global video_camera
        global global_frame

        if video_camera == None:
            video_camera = VideoCamera()

        while True:
            frame = video_camera.get_frame()

            if frame is not None:
                global_frame = frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

    def video_viewer(self):
        return Response(self.video_stream(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    def shape_to_np(self, shape, dtype="int"):

        coords = np.zeros((68, 2), dtype=dtype)
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        return coords

    def eye_on_mask(self, mask, side, shape):
        points = [shape[i] for i in side]
        points = np.array(points, dtype=np.int32)
        mask = cv2.fillConvexPoly(mask, points, 255)
        return mask

    def locatePupils(self, thresh, mid, img, right=False):
        cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        try:
            cnt = max(cnts, key=cv2.contourArea)
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            if right:
                cx += mid
            cv2.circle(img, (cx, cy), 8, ([17, 15, 100]), 1)
            return (cx, cy)
        except:
            pass

    def det(self, a, b):
        return a[0] * b[1] - a[1] * b[0]

    def mid1(self, p1, p2):
        return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

    def predi(self, xo, yo, param):
        p = []
        j = 0
        while (j <= len(xo) - 200):
            linie = []
            for i in range(j, j + 200):
                linie.append(xo[i])
                linie.append(yo[i])
            p.append(linie)
            j = j + 10

        loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
        norm = sklearn.preprocessing.normalize(p)
        predict = loaded_model.predict(norm)
        print(predict)

        s = 0.0
        for i in range(0, len(predict)):
            s = s + predict[i]
        mean = s / len(predict)

        result = Result(date=date.today(), results=predict, mean=mean, pacientId=param)
        return result

    def getResults(self, param):

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('C:\\Users\\Bianca\\PycharmProjects\\shape.dat')

        left = [36, 37, 38, 39, 40, 41]
        right = [42, 43, 44, 45, 46, 47]

        cap = cv2.VideoCapture('C:\\Users\\Bianca\\PycharmProjects\\FinalApp\\static\\video.avi')
        # cap = cv2.VideoCapture(0)
        _, img = cap.read()

        kernel = np.ones((9, 9), np.uint8)
        xo = [0]
        yo = [0]
        i = 0
        while (True):
            _, img = cap.read()
            i = i + 1
            if np.shape(img) != ():
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                rects = detector(gray)
                for rect in rects:
                    shape = predictor(gray, rect)
                    shape = self.shape_to_np(shape)
                    mask = np.zeros(img.shape[:2], dtype=np.uint8)
                    mask = self.eye_on_mask(mask, left, shape)
                    mask = self.eye_on_mask(mask, right, shape)
                    mask = cv2.dilate(mask, kernel, 5)
                    eyes = cv2.bitwise_and(img, img, mask=mask)
                    mask = (eyes == [0, 0, 0]).all(axis=2)
                    eyes[mask] = [255, 255, 255]
                    mid = (shape[42][0] + shape[39][0]) // 2
                    eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)
                    _, thresh = cv2.threshold(eyes_gray, 75, 255, cv2.THRESH_BINARY)
                    thresh = cv2.erode(thresh, None, iterations=2)  # 1
                    thresh = cv2.dilate(thresh, None, iterations=4)  # 2
                    thresh = cv2.medianBlur(thresh, 3)  # 3
                    thresh = cv2.bitwise_not(thresh)

                    midL = self.locatePupils(thresh[:, 0:mid], mid, img)
                    midR = self.locatePupils(thresh[:, mid:], mid, img, True)

                    landmarks = predictor(gray, rect)
                    left_point = (landmarks.part(36).x, landmarks.part(36).y)
                    right_point = (landmarks.part(39).x, landmarks.part(39).y)
                    center_top = self.mid1(landmarks.part(37), landmarks.part(38))
                    center_bottom = self.mid1(landmarks.part(41), landmarks.part(40))

                    left_point_r = (landmarks.part(42).x, landmarks.part(42).y)
                    right_point_r = (landmarks.part(45).x, landmarks.part(45).y)
                    center_top_r = self.mid1(landmarks.part(43), landmarks.part(44))
                    center_bottom_r = self.mid1(landmarks.part(47), landmarks.part(46))

                    a = int((left_point[0] + right_point[0]) / 2)
                    b = int((left_point[1] + right_point[1]) / 2)

                    c = int((left_point_r[0] + right_point_r[0]) / 2)
                    d = int((left_point_r[1] + right_point_r[1]) / 2)

                    if midL != None and midR != None:
                        xdiff = (a - midL[0], c - midR[0])
                        ydiff = (b - midL[1], d - midR[1])

                        div = self.det(xdiff, ydiff)
                        if div != 0:

                            line1 = ((a, b), midL)
                            line2 = ((c, d), midR)

                            d = (self.det(*line1), self.det(*line2))
                            x = self.det(d, xdiff) / div
                            y = self.det(d, ydiff) / div

                            inter = (int(x), int(y))
                            xo.append(inter[0])
                            yo.append(inter[1])

                            cv2.line(img, left_point, right_point, (0, 255, 0), 1)
                            cv2.line(img, center_top, center_bottom, (0, 255, 0), 1)
                            cv2.line(img, midL, inter, (0, 0, 255), 2)

                            cv2.line(img, left_point_r, right_point_r, (0, 255, 0), 1)
                            cv2.line(img, center_top_r, center_bottom_r, (0, 255, 0), 1)
                            cv2.line(img, midR, inter, (0, 0, 255), 2)

                        else:
                            xo.append(xo[len(xo) - 1])
                            yo.append(yo[len(yo) - 1])

                cv2.imshow('eyes', img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            else:
                break


        cap.release()
        cv2.destroyAllWindows()
        return self.predi(xo, yo, param)


cameraController = CameraController()

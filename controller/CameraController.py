import os

from flask import render_template, request, Response, jsonify
from flask import current_app

from utils.camera import VideoCamera


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
        dogS = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sound1.mp3')
        frog = os.path.join(current_app.config['UPLOAD_FOLDER'], 'frog.gif')
        video = os.path.join(current_app.config['UPLOAD_FOLDER2'], 'recorder2.js')
        return render_template('game.html', dog_image=dog, cat_image=cat, dog_sound=dogS, filename=video,
                               frog_image=frog)


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


cameraController = CameraController()

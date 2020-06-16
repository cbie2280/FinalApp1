from flask import Blueprint
from flask_login import login_required

from controller.CameraController import cameraController

mod3 = Blueprint("camera", __name__)



@mod3.route('/start', methods=['GET', 'POST'])
@login_required
def start():
    return cameraController.start()


@mod3.route('/record_status', methods=['POST'])
@login_required
def record_status():
    return cameraController.record_status()


@mod3.route('/video_viewer')
@login_required
def video_viewer():
    return cameraController.video_viewer()

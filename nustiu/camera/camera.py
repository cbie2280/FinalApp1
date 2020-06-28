from threading import Thread

from flask import Blueprint, render_template, current_app, request
from flask_login import login_required
from flask_login import current_user

from controller.CameraController import cameraController
# from app import celery
from utils.extensions import db

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


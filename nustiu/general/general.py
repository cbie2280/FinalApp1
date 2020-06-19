from threading import Thread

from flask import render_template, request
from flask_login import login_required, current_user

from app import app
from controller.CameraController import cameraController
from controller.UserController import generalController
from utils.extensions import db


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    return generalController.login()


@app.route('/logout')
def logout():
    return generalController.logout()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return generalController.register()


@app.route('/savepls')
@login_required
def save():
    def do_work(value):
        a=cameraController.pls(value)
        with app.app_context():
            db.session.add(a)
            db.session.commit()
        import time
        time.sleep(value)

    thread = Thread(target=do_work, kwargs={'value': request.args.get('value', current_user.id)})
    thread.start()
    return render_template('welldone.html', title='haha')

@app.route('/savepls1')
@login_required
def save1():
    def do_work(value):
        a=cameraController.pls(value)
        with app.app_context():
            db.session.add(a)
            db.session.commit()
        import time
        time.sleep(value)

    thread = Thread(target=do_work, kwargs={'value': request.args.get('value', current_user.id)})
    thread.start()
    return render_template('notsogood.html', title='haha')


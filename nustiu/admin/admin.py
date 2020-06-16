from flask import Blueprint
from flask_login import login_required

from controller.AdminController import adminController

mod4 = Blueprint("admin", __name__)


@mod4.route('/')
@mod4.route('/home2')
# @login_required
def home2():
    return adminController.home2()


@mod4.route('/admin', methods=['GET', 'POST'])
# @login_required
def admin():
    return adminController.admin()

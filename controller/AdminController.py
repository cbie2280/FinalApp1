from flask import render_template, redirect, url_for


class AdminController:

    def __init__(self):
        pass

    def home2(self):
        return redirect(url_for('admin.admin'))

    def admin(self):
        return render_template('admin.html')


adminController = AdminController()

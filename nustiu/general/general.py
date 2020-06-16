from app import app
from controller.UserController import generalController


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

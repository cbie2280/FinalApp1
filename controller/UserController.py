from flask import render_template, redirect, url_for
from flask_login import current_user

from forms1.LoginForm import LoginForm
from forms1.RegistrationForm import RegistrationForm
from repository.UserRepository import generalRepository


class UserController:

    def __init__(self):
        pass

    def login(self):
        form = LoginForm()
        if form.validate_on_submit():

            a = generalRepository.login(form.email.data, form.password.data, form.remember.data)
            if a == 0:
                return redirect(url_for('login'))
            elif a == 1:
                return redirect(url_for('patient.home1'))
            elif a == 3:
                print("fsdgdgds")
                return redirect(url_for('admin.home2'))
            else:
                return redirect(url_for('medic.home'))
        else:
            return render_template('login.html', title='Sign In', form=form)

    def logout(self):
        generalRepository.logout()
        return redirect(url_for('login'))

    def register(self):
        if current_user.is_authenticated:
            return redirect(url_for('medic.home'))

        form = RegistrationForm()
        if form.validate_on_submit():
            generalRepository.register(form.nume.data, form.prenume.data, form.email.data, form.parola.data)
            return redirect(url_for('login'))
        else:
            return render_template('signup.html', title='Inregistrare', form=form)


generalController = UserController()

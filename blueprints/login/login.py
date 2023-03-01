from flask import Blueprint, render_template, request, redirect, url_for
import flask_login
import os
# import flask

# import app instance of application
# from app import app


# ## Env
username = os.environ.get("APP_USER")
password = os.environ.get("APP_PASSWORD")

login_page = Blueprint('login_page', __name__, template_folder="templates")
login_manager = flask_login.LoginManager()



@login_page.record
def on_load(state):
    global app
    app = state.app
    login_manager.init_app(app)



users = {username: {'password': password}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form['email']
    if email in users and request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('admin'))
    return 'Bad login', 401

@login_page.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@login_page.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login_page.login')) , 302


#####################################################################APP ROUTES



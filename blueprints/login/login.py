from flask import Blueprint, render_template, request, redirect, url_for
import flask_login
import os
from blueprints.persona.persona import render_persona
import ast

#Env
full_users = os.environ.get("USERS")

login_page = Blueprint('login_page', __name__, template_folder="templates")
login_manager = flask_login.LoginManager()

@login_page.record
def on_load(state):
    global app
    app = state.app
    login_manager.init_app(app)

users = ast.literal_eval(full_users)


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


## admin page can render without limit
@login_page.route('/admin', methods=['GET'])
@flask_login.login_required
def admin():
    return render_template("loading.html", user=True) ### user=treu becouse we are logg in


@login_page.route('/adminR', methods=['GET']) #########this is here for the screen loader
@flask_login.login_required
def personaR():
    return render_persona(True)   ###### let the html know that this came from admin and not persona


@login_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html",)

    email = request.form['email']
    if email in users and request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('login_page.admin'))
    return 'Bad login', 401

@login_page.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@login_page.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login_page.login')) , 302




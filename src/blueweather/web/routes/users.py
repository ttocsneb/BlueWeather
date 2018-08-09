import urllib
import flask
from flask import url_for
import flask_login
from flask_login import login_required

from blueweather.web import forms, models
from blueweather.web import db, bcrypt

users = flask.Blueprint('users', __name__)


@users.route('/users/register', methods=['GET', 'POST'])
@login_required
def register():

    if flask_login.current_user.permissions.add_user is False:
        flask.flash("You do not have the privileges to access that page :/",
                    "danger")
        return flask.redirect(url_for('main.home'))

    form = forms.users.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = models.User(username=form.username.data,
                           password=hashed_password)

        # Create the permissions row for the user
        permissions = models.Permission(user_id=user.id)
        user.permissions = permissions

        # Add the rows to the database
        db.session.add(user)
        db.session.add(permissions)
        db.session.commit()

        flask.flash('Account created for {data}'.format(
            data=form.username.data), 'success')
        return flask.redirect(url_for('main.home'))

    return flask.render_template('user/register.html', title='Register',
                                 form=form)


@users.route('/users/login', methods=['GET', 'POST'])
def login():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(url_for('main.home'))

    form = forms.users.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            flask_login.login_user(user, remember=form.remember.data)
            next_page = flask.request.args.get('next', url_for('main.home'))
            return flask.redirect(next_page)
        flask.flash('Username or Password is incorrect', 'danger')

    return flask.render_template('user/login.html', title='Login', form=form)


@users.route('/users/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(url_for('main.home'))


@users.route('/users/account', methods=['GET', 'POST'])
@login_required
def settings():

    tabs = {
        'tabs': [{'name': 'permission', 'active': True, 'text': 'Permissions'},
                 {'name': 'password', 'active': False, 'text': 'Password'}],
        'current': 0
    }

    permissions = [
        {'text': 'Create Users',
         'checked': flask_login.current_user.permissions.add_user},
        {'text': 'Edit Permissions ',
         'checked': flask_login.current_user.permissions.change_perm},
        {'text': 'Edit System Settings',
         'checked': flask_login.current_user.permissions.change_settings},
        {'text': 'Reboot System',
         'checked': flask_login.current_user.permissions.reboot}
    ]

    change_password = forms.users.ChangePassword()

    if change_password.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            change_password.password.data).decode('utf-8')

        flask_login.current_user.password = hashed_password

        db.session.commit()

        flask.flash('Password Successfully Changed', 'success')
        return flask.redirect(url_for('users.settings'))

    if change_password.is_submitted():
        # Set the current tab to Password if the form was submitted and not
        # validated
        tabs['current'] = 1
        tabs['tabs'][0]['active'] = False
        tabs['tabs'][1]['active'] = True

    return flask.render_template('user/account.html', title='Account',
                                 permissions=permissions, tabs=tabs,
                                 form=change_password)


@users.route('/users/privileges', methods=['GET', 'POST'])
@login_required
def privileges():

    if flask_login.current_user.permissions.add_user is False:
        flask.flash("You do not have the privileges to access that page :/",
                    "danger")
        return flask.redirect(url_for('main.home'))

    # Edit User

    user = flask.request.args.get('user')

    if user:
        editUser = forms.permissions.EditUser()
        editUser.load(flask_login.current_user.id, int(user))
        if not editUser.check_valid():
            flask.flash('You cannot edit that user', category='warning')
            return flask.redirect(url_for('users.privileges'))

        user_name = models.User.query.filter_by(id=user).first().username

        if editUser.validate_on_submit():
            if editUser.setPrivileges():
                flask.flash("Successfully edited {user}'s permissions".format(
                    user=user_name), category='success')
            else:
                flask.flash("Could not edit that user's permissions",
                            category='danger')

            return flask.redirect(url_for('users.privileges'))

        editUser.load_defaults()

        return flask.render_template("user/permissions.html",
                                     title='Privileges', user=user_name,
                                     editUser=editUser)

    # Select User

    selectUser = forms.permissions.SelectUser()
    selectUser.users.choices = selectUser.getUsers()

    if selectUser.validate_on_submit():
        user_id = models.User.query.filter_by(
            id=selectUser.users.data).first().id

        return flask.redirect('{url}?{params}'.format(
            url=url_for('users.privileges'), params=urllib.parse.urlencode(
                {'user': user_id})))

    return flask.render_template('user/permissions.html', title='Privileges',
                                 selectUser=selectUser)

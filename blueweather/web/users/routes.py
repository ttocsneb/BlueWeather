import flask
from flask import url_for
import flask_login
from flask_login import login_required

from blueweather.web import db, bcrypt

from . import forms, models

users = flask.Blueprint('users', __name__)


@users.route('/users/register', methods=['GET', 'POST'])
@login_required
def register():

    if flask_login.current_user.permissions.add_user is False:
        flask.abort(403)

    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = models.User(username=form.username.data,
                           password=hashed_password)

        # Create the permissions row for the user
        perms = models.Permission(user_id=user.id)
        user.permissions = perms

        # Add the rows to the database
        db.session.add(user)
        db.session.add(perms)
        db.session.commit()

        flask.flash('Account created for {data}'.format(
            data=form.username.data), 'success')
        return flask.redirect(url_for('main.home'))

    return flask.render_template('user/register.jinja2', title='Register',
                                 form=form)


@users.route('/users/login', methods=['GET', 'POST'])
def login():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(url_for('main.home'))

    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            flask_login.login_user(user, remember=form.remember.data)
            next_page = flask.request.args.get('next', url_for('main.home'))
            return flask.redirect(next_page)
        flask.flash('Username or Password is incorrect', 'danger')

    return flask.render_template('user/login.jinja2', title='Login', form=form)


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

    perms = [
        {'text': 'Create Users',
         'checked': flask_login.current_user.permissions.add_user},
        {'text': 'Edit Permissions ',
         'checked': flask_login.current_user.permissions.change_perm},
        {'text': 'Edit System Settings',
         'checked': flask_login.current_user.permissions.change_settings},
        {'text': 'Reboot System',
         'checked': flask_login.current_user.permissions.reboot}
    ]

    change_password = forms.ChangePassword()

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

    return flask.render_template('user/account.jinja2', title='Account',
                                 permissions=perms, tabs=tabs,
                                 form=change_password)


@users.route('/users/privileges')
@login_required
def privileges():

    if flask_login.current_user.permissions.change_perm is False:
        flask.abort(403)

    all_users = models.User.query.all()

    usrs = [dict(
        id=u.id,
        name=u.username,
        add_user=u.permissions.add_user,
        change_perm=u.permissions.change_perm,
        change_settings=u.permissions.change_settings,
        reboot=u.permissions.reboot) for u in all_users]

    return flask.render_template('user/permissions.jinja2',
                                 title='Set Privileges',
                                 users=usrs)


@users.route('/users/privileges/set', methods=['POST'])
@login_required
def set_privileges():

    if flask_login.current_user.permissions.change_perm is False:
        flask.abort(403)

    data = flask.request.get_json()

    editor = flask_login.current_user
    # Check if the user is trying to edit himself
    if editor.id is data['id']:
        return 'false'
    perms = models.Permission.query.filter_by(
        user_id=data['id']).first()

    # Check if the edited user exists
    if perms is None:
        return 'false'

    print("Setting Privileges")

    editor_perm = editor.permissions

    # Only change the settings if the editor has the privileges to that setting
    if editor_perm.add_user:
        perms.add_user = data['add_user']
    if editor_perm.change_perm:
        perms.change_perm = data['change_perm']
    if editor_perm.change_settings:
        perms.change_settings = data['change_settings']
    if editor_perm.reboot:
        perms.reboot = data['reboot']

    db.session.commit()

    return 'true'

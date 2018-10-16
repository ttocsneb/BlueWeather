"""
User Forms
"""

from flask_wtf import FlaskForm
import flask_login
import wtforms
from wtforms import validators

from . import models


class RegistrationForm(FlaskForm):
    username = wtforms.StringField('Username', validators=[
        validators.DataRequired(),
        validators.Length(min=2, max=20)
    ])
    password = wtforms.PasswordField('Password', validators=[
        validators.DataRequired()
    ])
    conf_password = wtforms.PasswordField('Confirm Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('password')
    ])

    submit = wtforms.SubmitField('Sign Up')

    def validate_username(self, username):
        user = models.User.query.filter_by(username=username.data).first()
        if user:
            raise validators.ValidationError('That username is taken. ' +
                                             'Please choose a different one.')


class LoginForm(FlaskForm):
    username = wtforms.StringField('Username', validators=[
        validators.DataRequired(),
        validators.Length(min=2, max=20)
    ])
    password = wtforms.PasswordField('Password', validators=[
        validators.DataRequired()
    ])
    remember = wtforms.BooleanField('Remember Me')

    submit = wtforms.SubmitField('Login')


class ChangePassword(FlaskForm):
    password = wtforms.PasswordField('New Password', validators=[
        validators.DataRequired()
    ])
    conf_password = wtforms.PasswordField('Confirm Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('password')
    ])

    submit = wtforms.SubmitField('Change Password')


# Edit Permissions Forms


class SelectUser(FlaskForm):
    users = wtforms.RadioField("Select User", validators=[
        validators.InputRequired("You need to select a user to edit")],
        coerce=int)
    submit = wtforms.SubmitField("Edit User")

    def getUsers(self) -> list:
        found_users = models.User.query.all()

        choices = [(user.id, user.username)
                   for user in found_users
                   if flask_login.current_user.id is not user.id]

        return choices

from flask_wtf import FlaskForm
import wtforms
from wtforms import validators
import flask_login

from blueweather.web import models, db


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


class EditUser(FlaskForm):
    change_perm = wtforms.BooleanField(label='Edit Permissions')
    add_user = wtforms.BooleanField(label='Create Users')
    change_settings = wtforms.BooleanField(label='Edit System Settings')
    reboot = wtforms.BooleanField(label='Reboot System')

    submit = wtforms.SubmitField('Submit Changes')

    editor_id = 0
    user_id = 0

    def validate_privileges(self, field):
        if self.editor_id is self.user_id:
            raise validators.ValidationError(
                'You cannot edit your own privileges')
        num_users = models.User.query.filter_by(
            id=self.user_id).count()
        if num_users is 0:
            raise validators.ValidationError(
                'The user you are trying to edit does not exist')

    def load(self, editor_id: int, user_id: int):
        self.editor_id = editor_id
        self.user_id = user_id

    def check_valid(self) -> bool:
        if self.editor_id is self.user_id:
            return False

        editor_perm = models.Permission.query.filter_by(
            user_id=self.editor_id).first()
        permissions = models.Permission.query.filter_by(
            user_id=self.user_id).first()

        if editor_perm is None or permissions is None:
            return False

        if not editor_perm.change_perm:
            return False

        return True

    def load_defaults(self) -> bool:
        editor_perm = models.Permission.query.filter_by(
            user_id=self.editor_id).first()
        permissions = models.Permission.query.filter_by(
            user_id=self.user_id).first()

        if editor_perm is None or permissions is None:
            return False

        # Only allow the privileges that the current user has to be changed
        if not editor_perm.add_user:
            del self.add_user
        else:
            self.add_user.data = permissions.add_user
        if not editor_perm.change_perm:
            del self.change_perm
        else:
            self.change_perm.data = permissions.change_perm
        if not editor_perm.change_settings:
            del self.change_settings
        else:
            self.change_settings.data = permissions.change_settings
        if not editor_perm.reboot:
            del self.reboot
        else:
            self.reboot.data = permissions.reboot

        return True

    def setPrivileges(self) -> bool:
        if not self.check_valid():
            return False
        editor_perm = models.Permission.query.filter_by(
            user_id=self.editor_id).first()
        permissions = models.Permission.query.filter_by(
            user_id=self.user_id).first()

        print("Setting Privileges")

        if editor_perm.add_user:
            permissions.add_user = self.add_user.data
        if editor_perm.change_perm:
            permissions.change_perm = self.change_perm.data
        if editor_perm.change_settings:
            permissions.change_settings = self.change_settings.data
        if editor_perm.reboot:
            permissions.reboot = self.reboot.data

        db.session.commit()

        return True

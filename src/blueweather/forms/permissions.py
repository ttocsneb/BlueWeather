from flask_wtf import FlaskForm
import wtforms
from wtforms import validators
import flask_login

from blueweather import models, db


class SelectUser(FlaskForm):
    users = wtforms.RadioField("Select User", validators=[
        validators.InputRequired("You need to select a user to edit")],
                               coerce=int)
    submit = wtforms.SubmitField("Edit User")

    def getUsers(self) -> list:
        found_users: list = models.User.query.all()

        choices = [(user.id, user.username)
                   for user in found_users
                   if flask_login.current_user.id is not user.id]

        return choices


class Permission(FlaskForm):
    check = wtforms.BooleanField()

    def getData(self) -> bool:
        return self.check.data


class EditUser(FlaskForm):
    privileges = wtforms.FieldList(wtforms.FormField(Permission))
    submit = wtforms.SubmitField('Submit Changes')
    current_user = wtforms.StringField()

    editor_id = 0
    user_id = 0

    def validate_privileges(self, field):
        if self.editor_id is self.user_id:
            raise validators.ValidationError(
                'You cannot edit your own privileges')
        num_users: models.User = models.User.query.filter_by(
            id=self.user_id).count()
        if num_users is 0:
            raise validators.ValidationError(
                'The user you are trying to edit does not exist')

    def load(self, editor_id: int, user_id: int) -> bool:
        editor_perm: models.Permission = models.Permission.query.filter_by(
            user_id=editor_id).first()
        permissions: models.Permission = models.Permission.query.filter_by(
            user_id=user_id).first()

        if editor_id is None or permissions is None:
            return False

        self.editor_id = editor_id
        self.user_id = user_id
        # Only allow the privileges that the current user has to be changed

        i = 0
        length = len(self.privileges)
        orig = length is 0

        if editor_perm.add_user:
            if length <= i:
                self.privileges.append_entry()
                length += 1
            add_user = self.privileges[i]
            if orig:
                add_user.check.data = permissions.add_user
            add_user.check.label = "Create Users"
            add_user.check.name = 'add_user'
            i += 1

        if editor_perm.change_perm:
            if length <= i:
                self.privileges.append_entry()
                length += 1
            change_perm = self.privileges[i]
            if orig:
                change_perm.check.data = permissions.change_perm
            change_perm.check.label = 'Edit Permissions'
            change_perm.check.name = 'change_perm'
            i += 1

        if editor_perm.change_settings:
            if length <= i:
                self.privileges.append_entry()
                length += 1
            change_settings = self.privileges[i]
            if orig:
                change_settings.check.data = permissions.change_settings
            change_settings.check.label = 'Edit System Settings'
            change_settings.check.name = 'change_settings'
            i += 1

        if editor_perm.reboot:
            if length <= i:
                self.privileges.append_entry()
                length += 1
            reboot = self.privileges[i]
            if orig:
                reboot.check.data = permissions.reboot
            reboot.check.label = 'Reboot System'
            reboot.check.name = 'reboot'
            i += 1

        return True

    def setPrivileges(self, editor_id: int, user_id: int) -> bool:
        editor_perm: models.Permission = models.Permission.query.filter_by(
            user_id=editor_id).first()
        permissions: models.Permission = models.Permission.query.filter_by(
            user_id=user_id).first()

        if editor_id is None or permissions is None:
            return False

        print("Setting Privileges")

        perm: models.Permission
        for _ in range(len(self.privileges.entries)):
            perm = self.privileges.pop_entry()
            print("{id}={value}".format(id=perm.name, value=perm.getData()))
            if perm.name == 'add_user':
                if editor_perm.add_user:
                    permissions.add_user = perm.getData()
                    print("add_user: {perm}".format(perm=permissions.add_user))
                continue

            if perm.name == 'change_perm':
                if editor_perm.change_perm:
                    permissions.change_perm = perm.getData()
                    print("change_perm: {perm}".format(
                        perm=permissions.change_perm))
                continue

            if perm.name == 'change_settings':
                if editor_perm.change_settings:
                    permissions.change_settings = perm.getData()
                    print("change_settings: {perm}".format(
                        perm=permissions.change_settings))
                continue

            if perm.name == 'reboot':
                if editor_perm.reboot:
                    permissions.reboot = perm.getData()
                    print("reboot: {perm}".format(perm=permissions.reboot))
                continue

        db.session.commit()

        return True

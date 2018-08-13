
from flask_login import UserMixin
from blueweather.web import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    permissions = db.relationship('Permission', uselist=False, backref='user')

    def __repr__(self):
        return "User({id}: '{username}')".format(username=self.username,
                                                 id=self.id)


class Permission(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True,
                        nullable=False)
    change_perm = db.Column(db.Boolean, nullable=False, default=False)
    add_user = db.Column(db.Boolean, nullable=False, default=False)
    reboot = db.Column(db.Boolean, nullable=False, default=False)
    change_settings = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return ("Permission({user_id}: change_perm={change_perm}, add_user=" +
                "{add_user}, reboot={reboot}, change_settings=" +
                "{change_settings})").format(
                    user_id=self.user_id, change_perm=self.change_perm,
                    add_user=self.add_user, reboot=self.reboot,
                    change_settings=self.change_settings)

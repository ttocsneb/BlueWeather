from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from blueweather import forms
from blueweather.models import User, Permission
from blueweather import app, db, bcrypt

@app.route('/')
def home():
    breadcrumb = [
        {
            'name': 'Dashboard'
        }
    ]
    return render_template('dashboard.html', breadcrumbs=breadcrumb)


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():

    if current_user.permissions.add_user is False:
        flash("You do not have the privileges to access that page :/", "danger")
        return redirect(url_for('home'))

    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)

        # Create the permissions row for the user
        permissions = Permission(user_id=user.id)
        user.permissions = permissions

        # Add the rows to the database
        db.session.add(user)
        db.session.add(permissions)
        db.session.commit()

        flash('Account created for {data}'.format(data=form.username.data), 'success')
        return redirect(url_for('home'))


    return render_template('user/register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next', url_for('home'))
            return redirect(next_page)
        flash('Username or Password is incorrect', 'danger')


    return render_template('user/login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/settings')
@login_required
def settings():
    return render_template('user/account.html', title='settings')

@app.route('/privileges')
@login_required
def privileges():

    if current_user.permissions.add_user is False:
        flash("You do not have the privileges to access that page :/", "danger")
        return redirect(url_for('home'))

    return render_template('layouts/user.html', title='privileges')



@app.route('/weather')
def weather():
    breadcrumb = [
        {
            'name': 'Dashboard',
            'url': url_for('home')
        },
        {
            'name': 'weather'
        }
    ]
    return render_template('layouts/web.html', title='Weather', breadcrumbs=breadcrumb)


@app.route('/config')
@login_required
def config():
    breadcrumb = [
        {
            'name': 'Dashboard',
            'url': url_for('home')
        },
        {
            'name': 'config'
        }
    ]
    return render_template('layouts/web.html', title='Config', breadcrumbs=breadcrumb)

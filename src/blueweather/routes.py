from flask import render_template, url_for, flash, redirect

from blueweather import forms
from blueweather import app

@app.route('/')
def home():
    breadcrumb = [
        {
            'name': 'Dashboard'
        }
    ]
    return render_template('dashboard.html', breadcrumbs=breadcrumb)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()

    if form.validate_on_submit():
        flash('Account created for {data}'.format(data=form.username.data), 'success')
        return redirect(url_for('home'))


    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        if form.username.data == 'root' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        flash('Username or Password is incorrect', 'danger')


    return render_template('login.html', title='Login', form=form)

@app.route('/privileges')
def privileges():
    return render_template('layouts/user.html', title='privileges')

@app.route('/settings')
def settings():
    return render_template('layouts/user.html', title='settings')

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
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

# TODO: generate a secret key if the secret key doesn't already exist
app.config['SECRET_KEY'] = 'ec5b916be3348b6c695ced12ade929e9'

# Make the WSGI interface available at the top level so wfastcgi can get it
wsgi_app = app.wsgi_app

# server/
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
    form = RegistrationForm()

    if form.validate_on_submit():
        flash('Account created for {data}'.format(data=form.username.data), 'success')
        return redirect(url_for('home'))


    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.username.data == 'root' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Username or Password is incorrect', 'danger')


    return render_template('login.html', title='Login', form=form)

@app.route('/privileges')
def privileges():
    return render_template('user_layout.html', title='privileges')

@app.route('/settings')
def settings():
    return render_template('user_layout.html', title='settings')

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
    return render_template('layout.html', title='Weather', breadcrumbs=breadcrumb)

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
    return render_template('layout.html', title='Config', breadcrumbs=breadcrumb)

def main(debug=False):
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT, debug)


if __name__ == '__main__':
    main(True)
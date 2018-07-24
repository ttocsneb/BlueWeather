from flask import Flask, render_template, url_for
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it
wsgi_app = app.wsgi_app

breadcrumb_layout = [
    {
        'name': 'Home',
        'url': '/dashboard'
    },
    {
        'name': 'Dashboard'
    }
]

# server/
@app.route('/')
@app.route('/dashboard')
def hello():
    return render_template('dashboard.html', breadcrumbs=breadcrumb_layout)


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
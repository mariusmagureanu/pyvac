__author__ = 'mariusmagureanu'
from flask import Flask
from unrestricted.login_resource import login_blueprint
from restricted.user_resorce import user_blueprint


app = Flask(__name__)
app.register_blueprint(login_blueprint)
app.register_blueprint(user_blueprint, url_prefix='/user')


def run_flask():
    app.run(host='0.0.0.0', port=8182, threaded=True)

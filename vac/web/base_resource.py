__author__ = 'mariusmagureanu'
from flask import Flask
from unrestricted.login_resource import login_blueprint
from unrestricted.root_resource import root_blueprint
from restricted.user_resorce import user_blueprint
import os

app = Flask(__name__)
app.register_blueprint(login_blueprint)
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(root_blueprint)


def run():
    app.run(host='0.0.0.0', port=8182, threaded=True)
    #os._exit(0)


def run_flask():
    run()
    #new_pid = os.fork()
    #if new_pid == 0:
    #    run()

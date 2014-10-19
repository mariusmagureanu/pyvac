__author__ = 'mariusmagureanu'
from flask import Flask
from flask import request
from multiprocessing import Process
from unrestricted.login_resource import login_blueprint
from unrestricted.root_resource import root_blueprint
from restricted.user_resorce import user_blueprint
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.register_blueprint(login_blueprint)
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(root_blueprint)


def run_flask():
    app.run(host='0.0.0.0', port=8182, threaded=True, debug=False)

p = Process(target=run_flask)


def start_flask():
    p.name = "PyVacFlask"
    p.daemon = True
    p.start()


def stop_flask():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    p.terminate()
    p.join(timeout=2)



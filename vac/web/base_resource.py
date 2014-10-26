__author__ = 'mariusmagureanu'
from flask import Flask
from multiprocessing import Process
from unrestricted.login_resource import login_blueprint
from unrestricted.root_resource import root_blueprint
from restricted.user_resorce import user_blueprint
import logging

log = logging.getLogger('vac')
flask_log = logging.getLogger('werkzeug')
flask_log.setLevel(logging.ERROR)

app = Flask(__name__)
app.register_blueprint(login_blueprint)
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(root_blueprint)


def __run_flask():
    log.info("Starting Flask...")
    app.run(host='0.0.0.0', port=8182, threaded=True, debug=False)

flask_proc = Process(target=__run_flask)


def start_flask():
    flask_proc.name = "PyVacFlask"
    flask_proc.daemon = True
    flask_proc.start()


def stop_flask():
    flask_proc.terminate()
    flask_proc.join(timeout=2)
    log.info("Flask stopped.")

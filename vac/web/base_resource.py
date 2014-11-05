from vac.web.services.login_resource import login_blueprint
from vac.web.services.user_resorce import user_blueprint
from flask import Flask
from vac.web.services.root_resource import root_blueprint
from multiprocessing import Process
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
    app.secret_key = 'my credit card pin number, ofcourse.'
    app.run(host='0.0.0.0', port=8182, threaded=True)

flask_proc = Process(target=__run_flask)


def start_flask():
    flask_proc.name = "PyVacFlask"
    flask_proc.daemon = True
    flask_proc.start()


def stop_flask():
    flask_proc.terminate()
    flask_proc.join(timeout=2)
    log.info("Flask stopped.")

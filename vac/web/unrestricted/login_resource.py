__author__ = 'mariusmagureanu'
import time
from flask import Blueprint, request, json
from twisted.internet import defer

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/test', methods=['GET'])
def test():
    return "VacPi's alive!\n"


@login_blueprint.route('/wait', methods=['GET'])
def wait():
    output = "Ok\n"
    try:
        d = defer.Deferred()
        d.addCallback(__sleep)
        d.callback("stuff")
    except Exception as e:
        output = e.message + "\n"
    return output


@login_blueprint.route('/login', methods=['POST'])
def login():
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data + "\n"

    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)


def __sleep(text):
    time.sleep(1)
    print text
    return "Back on track...\n"

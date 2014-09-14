__author__ = 'mariusmagureanu'
from flask import Blueprint, Response

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/save', methods=['POST'])
def save():
    return Response(status=201)

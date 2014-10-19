__author__ = 'mariusmagureanu'
from flask import Blueprint, request, Response, json
from vac.dao.facade.node_facade import NodeFacade
from vac.dao.entities.model import Node


root_blueprint = Blueprint('root', __name__)
__node_facade = NodeFacade()


@root_blueprint.route('/register', methods=['PUT'])
def register_node():
    json_agent = json.loads(request.data)
    port = json_agent['port']
    password = json_agent['password']
    dash = json_agent['dash-n']
    user = json_agent['user']
    host = request.headers['Host']
    n = Node(agent_host=port, agent_username=user, agent_password=password, dash_n=dash, name='localhost:'+port)
    __node_facade.save(n)
    return Response('Ok', 201, mimetype='text/plain')


@root_blueprint.route('/stats', methods=['PUT'])
def push_stats():
    print request.data
    return Response('Ok', 201, mimetype='text/plain')


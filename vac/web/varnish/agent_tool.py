__author__ = 'mariusmagureanu'
import base64
import httplib
import urllib


class AgentTool(object):

    __agent_functions = dict(
        ping=('ping', ['GET',str]),
        direct=('direct', ['POST',str, bool]),
        stats=('stats', ['GET']),
        ban=('ban', ['GET',str]),
        vcljson=('vcljson/', ['GET', int]),
        vcl=('vcl', ['GET',int]),
        vcldeploy=('vcldeploy', ['PUT', int]),
        vcl1=('vcl', ['GET',int]),
        param=('param', ['GET',int]),
        start=('start', ['PUT']),
        stop=('stop', ['PUT']),
        paramjson=('paramjson', ['GET']),
        status=('status', ['GET']),
        panic=('panic', ['GET',str, int]),
        echo=('echo',['GET']),
        help=('', ['GET']))

    def __getattr__(self, item):
        if item in self.__agent_functions:
            function_name, function_args = self.__agent_functions[item]

            def wrapper(*args):
                return self.__agent_factory("127.0.0.1", 6085, function_name, args, function_args)
            return wrapper

    def __agent_factory(self, host, port, fname, args, f_args):
        method = f_args[0]
        conn = httplib.HTTPConnection(host, port)
        conn.connect()
        auth = base64.encodestring("agent:pass")
        header = "Basic " + auth.strip()
        headers = {"Authorization": header}
        params = urllib.urlencode({'spam': 1, 'eggs' :2, 'shit': 0})
        conn.request(method, "/"+fname, None, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        print response.status, response.reason
        return data


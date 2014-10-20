__author__ = 'mariusmagureanu'
from twisted.internet import defer, reactor
from twisted.web.client import Agent
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol

import time
import crochet
import json
import base64
import threading
import logging

log = logging.getLogger('vac')
request_timeout = 3


def _chain_timeout(deferred, seconds, msg=None):
    if seconds is None:
        seconds = 0
    timed_deferred = TimedDeferred(seconds, msg=msg)
    deferred.addCallback(__safe_call_deferred, timed_deferred)
    deferred.addErrback(__safe_err_deferred, timed_deferred)
    return timed_deferred


def __safe_call_deferred(value, deferred):
    if not deferred.called:
        deferred.callback(value)


def __safe_err_deferred(value, deferred):
    if not deferred.called:
        deferred.errback(value)


class AgentTool(object):

    def __init__(self):
        from vac.dao.facade.node_facade import NodeFacade
        from vac.dao.facade.group_facade import GroupFacade
        self.__node_facade = NodeFacade()
        self.__group_facade = GroupFacade()
        self.__nodes = None
        self.__current_node = None
        self.__groups = None
        self.__reactor = reactor
        crochet._main._reactor = self.__reactor
        self.__event = threading.Event()
        self.__agent = Agent(self.__reactor)
        self.__start_reactor()

    def __getattr__(self, item):
        if item in self.__agent_functions:
            function_name, function_args = self.__agent_functions[item]

            def wrapper(*cli_args):
                return self.__do_request("localhost", function_name, cli_args, function_args)
            return wrapper

    __agent_functions = dict(
        ping=('ping', ['GET', str]),
        direct=('direct', ['POST', str, bool]),
        stats=('stats', ['GET']),
        ban=('ban', ['GET', str]),
        vcljson=('vcljson/', ['GET', int]),
        vcl=('vcl', ['GET', int]),
        vcldeploy=('vcldeploy', ['PUT', int]),
        vcl1=('vcl', ['GET', int]),
        param=('param', ['GET', int]),
        start=('start', ['PUT']),
        stop=('stop', ['PUT']),
        paramjson=('paramjson', ['GET']),
        status=('status', ['GET']),
        panic=('panic', ['GET', str, int]),
        echo=('echo', ['GET']),
        help=('', ['GET']))

    def __create_daemon_thread(self, *args, **kwargs):
        t = threading.Thread(*args, **kwargs)
        t.setDaemon(True)
        return t

    def __start_reactor(self):
        """
        starts the reactor in a thread and waits for it to start.
        """
        # <HACK>: Override threadpool's threads to be daemons
        from twisted.python import threadpool
        threadpool.ThreadPool.threadFactory = self.__create_daemon_thread
        crochet.setup()
        logging.getLogger('twisted').setLevel(logging.ERROR)
        self.__reactor.callFromThread(self.__event.set)
        self.__event.wait()

    def __on_request_result(self, response):
        print("Got response: {}".format(response))
        return True

    def __do_request(self, host, f_name, cli_args, f_args):
        '''

        :param host:
        :param f_name:
        :param cli_args:
        :param f_args:
        :return:
        '''

        method = f_args[0]

        if cli_args:
            for a_port, u_name, u_pass in self.__group_facade.get_nodes_as_tuples(cli_args[0]):
                self.__do__(host=host, port=a_port, fname=f_name,
                            method=method, username=u_name, user_pass=u_pass)
        elif self.__current_node.agent_host is not None:
            self.__do__(host=host, port=self.__current_node.agent_host, fname=f_name,
                        method=method, username="agent", user_pass="pass")
        else:
            print 'No node selected, use <set_curent_node> to choose one.'

    def __do__(self, host, port, fname, method, username, user_pass):
        '''

        :param host:
        :param port:
        :param fname:
        :param method:
        :param username:
        :param user_pass:
        :return:
        '''
        from twisted.web.http_headers import Headers
        auth = base64.encodestring("%s:%s" % (username, user_pass))
        header = "Basic " + auth.strip()
        headers = {"Authorization": [header]}
        req_defered = self.__agent.request(
            method=method,
            uri="http://%s:%s/%s" % (host, str(port), fname),
            headers=Headers(headers))

        chained_req = _chain_timeout(req_defered, request_timeout)

        @chained_req.addErrback
        def on_error(failure):
            print 'Got failure: ', failure
            return failure

        @chained_req.addCallback
        def on_result(response):
            done = Deferred()
            done.addCallback(self.__on_request_result)
            response.deliverBody(BeginningPrinter(done))

    def list_nodes(self, group_name=None):
        '''

        :return:
        '''
        if group_name:
            t = self.__group_facade.get_nodes_as_tuples(group_name)
            nodes = [n[3] for n in t]
            return nodes
        else:
            self.__nodes = self.__node_facade.all()
            nodes = json.loads(self.__nodes.to_json())
            node_names = [node['name'] for node in nodes]
            return node_names

    def list_groups(self):
        '''

        :return:
        '''
        self.__groups = self.__group_facade.all()
        groups = json.loads(self.__groups.to_json())
        group_names = [group['name'] for group in groups]
        return group_names

    def remove_node(self, node_name):
        '''

        :param node_name:
        :return:
        '''
        if self.__nodes:
            sel_node = [n for n in self.__nodes if n.name == node_name]
            self.__node_facade.remove(sel_node[0])
        else:
            self.__node_facade.delete_by_field('name', node_name)

    def remove_group(self, group_name):
        '''

        :param group_name:
        :return:
        '''
        if self.__groups:
            sel_group = [g for g in self.__groups if g.name == group_name]
            self.__group_facade.remove(sel_group[0])
        else:
            self.__group_facade.delete_by_field('name', group_name)

    def clear_nodes(self):
        '''

        :return:
        '''
        self.__node_facade.clear_all()

    def clear_groups(self):
        '''

        :return:
        '''
        self.__group_facade.clear_all()

    def set_current_node(self, node_name):
        '''

        :param node_name:
        :return:
        '''
        if self.__nodes:
            sel_node = [n for n in self.__nodes if n.name == node_name]
            if sel_node:
                self.__current_node = sel_node[0]
        else:
            self.__current_node = self.__node_facade.find_one_based_on_field('name', node_name)

        if self.__current_node:
            print "You have selected node: %s" % self.__current_node.name
        else:
            print "Node %s not found." % node_name

    def create_group(self, group_name):
        '''

        :param group_name:
        :return:
        '''
        self.__group_facade.create_group(name=group_name)

    def add_node_to_group(self, node_name, group_name):
        '''

        :param node_name:
        :param group_name:
        :return:
        '''
        self.__group_facade.add_cache(cache_name=node_name, group_name=group_name)

    def remove_node_from_group(self, node_name, group_name):
        '''

        :param node_name:
        :param group_name:
        :return:
        '''
        self.__group_facade.remove_cache(cache_name=node_name, group_name=group_name)

    def remove_all_nodes_in_group(self, group_name):
        '''

        :param group_name:
        :return:
        '''
        self.__group_facade.clear_caches(group_name)


class TimedDeferred(defer.Deferred):

    '''A Deferred that automatically errbacks with a TimeoutError on timeout.
    '''

    def __init__(self, seconds=None, msg=None):
        '''
        :parameter seconds: the timeout after which this TimedDeferred will
            errback with a TimeoutError. If specified the defered will start
            counting down to the timeout immediately.
        :parameter msg: optional message to display when timeout occurs.
        '''
        defer.Deferred.__init__(self)
        self._timeout_seconds = None
        self._finish_time = None
        self._timer = None
        self._has_timed_out = False
        self.msg = msg
        if seconds is not None:
            self.setTimeout(seconds)

    def setTimeout(self, seconds, msg=None):
        '''Sets the timeout on the TimedDeferred **and starts the timer**.

        :parameter seconds: the timeout, in seconds, after which this
            TimedDeferred will errback with a TimeoutError.
        :parameter msg: optional message to display when timeout occurs.
        '''
        if self.called:
            return
        if self._timer is not None:
            raise Exception(
                "Can't call setTimeout twice on the same Deferred.")

        if msg is not None:
            self.msg = msg
        self._timeout_seconds = seconds
        self._timer = reactor.callLater(self._timeout_seconds,
                                        lambda: self.called or self._do_timeout())
        return self._timer

    def _do_timeout(self):
        self._has_timed_out = True
        msg = str(self)
        if self.msg:
            msg += ': %s' % self.msg
        self.errback(Exception(msg))

    def isTimerActive(self):
        return self._timer is not None and self._timer.active()

    def errback(self, failure):
        self._finish_time = time.time()
        if self.isTimerActive():
            self._timer.cancel()
        return defer.Deferred.errback(self, failure)

    def callback(self, result):
        self._finish_time = time.time()
        if self.isTimerActive():
            self._timer.cancel()
        return defer.Deferred.callback(self, result)

    def __str__(self):
        basic_str = '<%s at %s: {}>' % (self.__class__.__name__, hex(id(self)))
        if self.isTimerActive():
            remaining = self._timer.getTime() - time.time()
            return basic_str.format('running, %.1fs remaining' % remaining)
        elif self._timeout_seconds is None:
            return basic_str.format('timeout not set')
        elif self._has_timed_out:
            return basic_str.format(
                'timed out after %.1fs' % self._timeout_seconds)
        elif self.called:
            remaining = self._timer.getTime() - self._finish_time
            return basic_str.format('completed, %.1fs spare' % remaining)


class BeginningPrinter(Protocol):

    def __init__(self, finished):
        self.finished = finished
        self.remaining = 1024 * 10
        self.total_response = ""

    def dataReceived(self, bytes_sent):
        if self.remaining:
            display = bytes_sent[:self.remaining]
            self.total_response += display
            self.remaining -= len(display)
        return bytes_sent

    def connectionLost(self, reason):
        self.finished.callback(self.total_response)
        return reason

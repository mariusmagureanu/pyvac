__author__ = 'mariusmagureanu'
import os
import sys
import logging
import colorama

from cStringIO import StringIO
from .config import EngineConfig
from vac.dao.mongo.connector import connect_to_mongo
from vac.web.base_resource import start_flask, stop_flask

logging.basicConfig(filename='vac.log',
                    level=logging.INFO,
                    filemode='w')
log = logging.getLogger('vac')


class Engine(object):

    def __init__(self):
        self.running = False
        self.config = EngineConfig()
        self._exit_status = None

    def _make_unique_log_dir(self, desired_logdir, counter_limit=500):
        '''Makes a unique log directory based on the desired_logdir path. We
        will append _n (where n<= 500) to the basename as required to make sure
        we don't overwrite an existing directory.
        '''
        logdirectory = desired_logdir
        counter = 0
        while True:
            try:
                os.makedirs(logdirectory)
            except OSError:
                counter += 1
                if counter == counter_limit:
                    raise
                else:
                    logdirectory = '{}_{:d}'.format(desired_logdir, counter)
            else:
                return logdirectory

    def _make_log_dir(self):
        logdirectory = self.config['desired_logdir']
        if not self.config['overwrite_logdir']:
            logdirectory = self._make_unique_log_dir(logdirectory)
        elif not os.path.exists(logdirectory):
            os.makedirs(logdirectory)
        self.config['logdirectory'] = logdirectory

    def initialise_logging(self):
        colorama.init()
        if self.config['store_logs']:
            self._make_log_dir()
            eventlog_file = self.get_fp('eventlog.log')
        else:
            eventlog_file = StringIO()

    def teardown_logging(self):
        loggers = [logging.root]
        if self.config['store_logs']:
            log.info('VAC logdirectory={!r}'.format(
                os.path.abspath(self.config['logdirectory'])))
            targeted_loggers = [logging.getLogger(logname) for logname in (
                'statemachine', 'protocol', 'vac', 'backend',
                'feedback')]
            loggers.extend(targeted_loggers)
        # This is the last moment a log will be available:
        logging.info('Goodbye!')
        for logger in loggers:
            while logger.handlers:
                logger.removeHandler(logger.handlers[0])

    def get_fp(self, *filename):
        file_path = os.path.join(self.config['logdirectory'],
                                 *filename)
        return open(file_path, 'w')

    def _get_test_name(self):
        if self.config['runfile']:
            return os.path.splitext(
                os.path.basename(self.config['runfile']))[0]
        else:
            return 'VacPi'

    def set_exit_status(self, reason=None):
        '''Sets the value which the engine will pass to sys.exit once it's done
        with cleanup.
        '''
        self._exit_status = reason

    def start(self, runtime_config=None):
        connect_to_mongo()
        self.config.update_current_config(runtime_config)
        if self.running:
            return
        # self.initialise_logging()

        log.info('Starting Vac Pi version=0.1')
        self.running = True
        start_flask()

    def stop(self):
        if not self.running:
            return self._exit_status
        self.running = False
        stop_flask()

        return self._exit_status

    def perform_exit(self):
        if self.config['has_runfile'] or self.config['should_exit']:
            sys.exit(self._exit_status)

    def get_metadata_dict(self):
        version_info = self.config.get_vac_version_info()
        return {
            'version': version_info.get('version', 'Unknown'),
            'date': version_info.get('date', 'Unknown'),
            'python_version': sys.version.replace('\n', ' '),
            'setupfile': self.config['setupfile'],
            'runfile': self.config['runfile'],
            'defines': self.config['defines']}


def run(function, config=None, args=None, kwargs=None, engine=None):

    engine = engine or get_engine()
    engine.start(config)
    args = args or []
    kwargs = kwargs or {}
    log.debug('Running test function %r (args=%r, kwargs=%r)' % (
        function, args, kwargs))
    try:
        result = function(*args, **kwargs)
    except KeyboardInterrupt:
        message = 'Keyboard interrupt whilst running test function %r' % (
            function.__name__)
        log.warning(message)
        engine.set_exit_status(message)
    except Exception:
        message = 'Test function %r failed' % function.__name__
        log.exception(message)
        engine.set_exit_status(message)
    else:
        log.debug('Finished running test function %r' % function)
        return result
    finally:
        engine.stop()

_engine = Engine()
_engine_proxy = None


def get_engine():
    return _engine


def get_engine_proxy():
    global _engine_proxy
    if not _engine_proxy:
        return _engine_proxy

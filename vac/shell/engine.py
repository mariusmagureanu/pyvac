__author__ = 'mariusmagureanu'
import os
import sys
import time
import logging
import colorama
import crochet

from cStringIO import StringIO
from config import EngineConfig
from vac.dao.mongo.connector import connect_to_mongo
from vac.web.base_resource import run_flask
from twisted.internet import reactor


log = logging.getLogger('vac')


class Engine(object):
    '''The component responsible for starting and stopping the frontend
    and backend

    Note: this object also holds the proxy and the backend service.

    '''
    def __init__(self, reactor=reactor):
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
            #self._setup_targeted_log_files(self.config['logdirectory'])
            eventlog_file = self.get_fp('eventlog.log')
        else:
            eventlog_file = StringIO()
        '''
        self.state.eventlog = eventlog.EventLog(eventlog_file)
        stdout_handler = logger.enable_first_run_logging(
            self.config)
        self.state.stdout_handler = stdout_handler
        self.state.logtransport = logger.enable_standard_logging(
            self.config)
        if self.config['logdirectory']:
            log.info('TNG logdirectory=%r' % os.path.abspath(
                self.config['logdirectory']))

    def _setup_targeted_log_files(self, logdirectory):
        statemachine = LogHandler(logdirectory, 'statemachine.log')
        logging.getLogger('statemachine').addHandler(statemachine)
        statemachine.setLevel(logging.DEBUG)
        protocol = LogHandler(logdirectory, 'protocol.log')
        logging.getLogger('protocol').addHandler(protocol)
        protocol.setLevel(logging.DEBUG)
        tng = LogHandler(logdirectory, 'tng_frontend.log')
        logging.getLogger('tng').addHandler(tng)
        tng.setLevel(logging.DEBUG)
        backend_ = LogHandler(logdirectory, 'backend.log')
        logging.getLogger('backend').addHandler(backend_)
        backend_.setLevel(logging.DEBUG)
        feedback = LogHandler(logdirectory, 'feedback.log')
        logging.getLogger('feedback').addHandler(feedback)
        logging.getLogger('Call.Signal').addHandler(feedback)
        logging.getLogger('statemachine').addHandler(feedback)
        feedback.setLevel(logging.DEBUG)
        twisted = LogHandler(logdirectory, 'twisted.log')
        logging.getLogger('twisted').addHandler(twisted)
        twisted.setLevel(logging.DEBUG)
'''

    def teardown_logging(self):
        loggers = [logging.root]
        if self.config['store_logs']:
            log.info('TNG logdirectory={!r}'.format(
                os.path.abspath(self.config['logdirectory'])))
            targeted_loggers = [logging.getLogger(logname) for logname in (
                'statemachine', 'protocol', 'tng', 'backend',
                'feedback', 'Call.Signal', 'twisted')]
            loggers.extend(targeted_loggers)
        # This is the last moment a log will be available:
        log.info('Goodbye!')
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
            return 'TNGPi'

    def set_exit_status(self, reason=None):
        '''Sets the value which the engine will pass to sys.exit once it's done
        with cleanup.
        '''
        self._exit_status = reason

    def save_scripts(self):
        scriptfolder = os.path.join(self.config['logdirectory'], 'scriptfiles')
        if not os.path.exists(scriptfolder):
            os.makedirs(scriptfolder)
        runfile_copy = self.get_fp('scriptfiles', 'runfile')
        if self.config['runfile'] and os.path.exists(self.config['runfile']):
            runfile_data = open(self.config['runfile']).read()
            runfile_copy.write(runfile_data)
        runfile_copy.close()
        setupfile_copy = self.get_fp('scriptfiles', 'setupfile')
        if self.config['setupfile'] and os.path.exists(
                self.config['setupfile']):
            setupfile_data = open(self.config['setupfile']).read()
            setupfile_copy.write(setupfile_data)
        setupfile_copy.close()

    def start(self, runtime_config=None):
        connect_to_mongo()

        self.config.update_current_config(runtime_config)
        if self.running:
            #If we have already started we just reconfigure
            #and return control
            return
        self.initialise_logging()
        log.info('Starting TNG Pi version=%r', self.config.get_tng_version())
        if self.config['store_logs']:
            self.save_scripts()
        #initialise_device_types_and_interfaces()
        device_setups = None
        if self.config['setupfile'] is not None:
            try:
                pass
               # device_setups = setupfile_parser.parse_setupfile(
               #     self.config['setupfile'],
               #     self.device_factory.device_names)
            except Exception as e:
                log.exception('Failed to parse setup file: {}'.format(e))
                sys.exit(1)
        if device_setups:
            crochet.wait_for_reactor(
                self.device_factory.create_devices)(device_setups)
        self.running = True
        #run_flask()

    def stop(self):
        if not self.running:
            return self._exit_status
        #self.state.stop_time = time.time()
        #crochet.wait_for_reactor(self.device_factory.cleanup)()
        #self.teardown_logging()
        self.running = False
        return self._exit_status

    def perform_exit(self):
        if self.config['has_runfile'] or self.config['should_exit']:
            sys.exit(self._exit_status)

    def get_metadata_dict(self):
        version_info = self.config.get_tng_version_info()
        return {
            'version': version_info.get('version', 'Unknown'),
            'date': version_info.get('date', 'Unknown'),
            'python_version': sys.version.replace('\n', ' '),
            'setupfile': self.config['setupfile'],
            'runfile': self.config['runfile'],
            'defines': self.config['defines']}

    def log_to_devices(self, message):
        '''This method is used to put general TNG log notifications out to all
        devices in a test. **Use sparingly!**

        :parameter message: The string to log on all the devices.
        '''
        devices = self.device_factory.devices
        if devices:
            from tng.api import concurrent
            concurrent(
                [self._get_try_log_to_device(
                    device, message) for device in devices],
                raise_on_error=False)

    def _get_try_log_to_device(self, device, message):
        def try_log_to_device():
            try:
                device.log_to_device(message)
            except Exception:
                log.debug(
                    'WARNING: Could not log message to device {!r}'.format(
                        device))
        return try_log_to_device


def run(function, config=None, args=None, kwargs=None, engine=None):
    '''The main entry point for running your code within a running |TNG|
    :class:`~tng.frontend.engine.Engine`.

    :parameter function: the function to run
    :parameter config: dictionary of runtime configuration items as parsed by
        the ``tng.frontend.option_parser``
    :parameter args: optional positional arguments to pass to ``function``
    :parameter kwargs: optional keyword arguments to pass to ``function``

    Before executing your function |tng| will be started. This involves (if
    necessary) creating the test log directory, configuring logging, parsing
    any setup file and starting the twisted reactor in the backend. |tng| then
    creates all required devices using any setup parameters supplied.

    Once |tng|'s :class:`~tng.frontend.engine.Engine` is running, we then call
    your function with the supplied positional and keyword value arguments, and
    handle any exceptions raised (including ``KeyboardInterrupt`` from
    ``ctrl+c``).

    .. seealso::

        :func:`tng.api.runner` - wrapper for invoking unittest-based
        tests via :func:`tng.run`.
    '''
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
        #_engine_proxy = TwistedProxy(get_engine())
        return _engine_proxy

__author__ = 'mariusmagureanu'

import logging
import time
import os

log = logging.getLogger('frontend.config')


def format_loglevel(level):
    if isinstance(level, str):
        if level.isdigit():
            level = logging.getLevelName(int(level))
        else:
            level = level.upper()
    else:
        level = logging.getLevelName(level)

    return level


class EngineConfig(object):

    '''An object that holds the config for the current VAC session.
    '''

    def __init__(self):
        self._config_data = {
            'defines': {},
            'desired_logdir': None,
            'logdirectory': None,
            'overwrite_logdir': False,
            'loglevel': logging.INFO,
            'vacpi_version_info': '0.1',
            'crash_on_boot': True,
            'setupfile': None,
            'runfile': None,
            'should_exit': True,
            'has_runfile': False,
            'run_mode': 'vanilla',
            'store_logs': True,
            'logbase': 'vac_log',
            'username': 'marius',
            'shell': 'ipython',
            'color_output': True,
        }

    def __getitem__(self, key):
        if key == 'loglevel':
            return format_loglevel(self._config_data[key])
        else:
            return self._config_data[key]

    def __setitem__(self, key, value):
        if key not in self._config_data:
            raise KeyError('Tried to set a non-existent configuration item')
        self._config_data[key] = value

    def get_config_dict(self):
        '''
        :returns: sanitised dictionary of current config.
        Note: loglevel object is converted to a more meaningful level name
                string (e.g. logging.INFO -> 'INFO')
        '''
        config = self._config_data.copy()
        if 'loglevel' in config:
            config['loglevel'] = format_loglevel(config['loglevel'])
        return config

    def update_current_config(self, runtime_config):
        '''Merge the config given to vac.run by the user
        with the default/user specified (vacrc) config values
        '''
        if not runtime_config:
            runtime_config = {}
        self._config_data.update(runtime_config)
        # expand out ~ to user's home
        self['logbase'] = os.path.expanduser(self['logbase'])
        if self['store_logs'] and not self['desired_logdir']:
            self['desired_logdir'] = self.generate_log_directory_name()

    def generate_log_directory_name(self):
        logpaths = [self['logbase'], self['username'],
                    time.strftime('%Y%m%d-%H%M%S')]
        return os.path.join(*logpaths)

    def get_vac_version_info(self):
        '''Returns a dictionary of VAC Pi version info.

        For example dict(version='v3.1.7-2-gdf4e1ec',
                         date='2012-08-31 00:21:24 +0100')
        '''
        if self['vacpi_version_info'] is None:
            try:
                self['vacpi_version_info'] = '0.1'
            except Exception as e:
                log.debug('Failed to fetch vacpi git revision: %s', e)
                self['vacpi_version_info'] = dict(
                    version='Unknown', date='Unknown')
        return self['vacpi_version_info']

    def get_vac_version(self):
        '''Returns the VAC version (or 'Unknown' if no version available).
        '''
        version_info = self.get_vac_version_info()
        return version_info

__author__ = 'mariusmagureanu'
#!/usr/bin/env python
import traceback
import logging
import code
import vac.web.varnish.agent_tool
from engine import get_engine, run

log = logging.getLogger('VacShell')


class VacShell(object):
    header = '''Welcome to Vac Pi interactive shell.
    Hit Ctrl-D to exit.'''

    def __init__(self):
        self.engine = get_engine()
        self.config = self.engine.config

    def get_shell(self, shell_name=None):
        local_ns = locals()
        local_ns['vac'] = vac

        def make_default_shell():
            def _shell(header=None, locals_=None):
                if locals_ is not None:
                    local_ns.update(locals_)
                shell = code.InteractiveConsole(locals=local_ns)
                return shell.interact(banner=header)
            return _shell

        if shell_name == 'ipython':
            self.monkey_patch_ipython_history_manager()
            def make_shell():
                # TODO: restrict user namespace to just 'vac' etc
                try:
                    import IPython.Shell
                    shell = IPython.Shell.IPShellEmbed(argv='', user_ns='vac.web.varnish.agent_tool')
                except ImportError:
                    # IPython 0.11+
                    # - Note: ipython 0.11 prints out a proper "Python..."
                    # banner while ipython 0.10 does not??
                    try:
                        from IPython.frontend.terminal.embed import (
                            InteractiveShellEmbed)
                        shell = InteractiveShellEmbed()
                    except ImportError:
                        return None
                def ipython_shell(header=None, locals_=None):
                    # Note: IPython doesn't default global_ns to anything
                    # sensible so we need to define it or else scoping breaks
                    # in inner scopes, e.g. def func(): print outer Also,
                    # unless we pass in locals() as local_ns it also fails! No
                    # idea why.
                    if locals_ is not None:
                        local_ns.update(locals_)
                    return shell(header=header, local_ns=local_ns,
                                 global_ns=local_ns)
                return ipython_shell

        elif shell_name == 'bpython':
            def make_shell():
                import bpython
                shell = bpython.embed
                def bpython_shell(header=None, locals_=None):
                    if locals_ is not None:
                        local_ns.update(locals_)
                    shell(banner=header, locals_=local_ns)
                return bpython_shell
        else:
            make_shell = make_default_shell

        try:
            shell = make_shell()
        except Exception:
            shell = None
        finally:
            if not shell:
                log.warn('Unable to create a Vac shell using %s; falling '
                         'back on the default Python shell' % shell_name)
                shell = make_default_shell()

        return shell

    def monkey_patch_ipython_history_manager(self):
        '''bug https://github.com/ipython/ipython/issues/680
        IPython 0.11 will re-initialise the history manager's sqlite3 db
        connection when displaying exception tracebacks (in our TNG Pi
        thread), then try to use it on Python exit which sqlite3 rejects
        unless we use
            check_same_thread=False
        '''
        try:
            from IPython.core.history import HistoryManager
            import sqlite3
            old_init_db = HistoryManager.init_db

            def patched_init_db(self):
                old_init_db(self)
                self.db = sqlite3.connect(
                    self.hist_file, check_same_thread=False)
            HistoryManager.init_db = patched_init_db
        except ImportError:
            pass

    def get_shell_func(self):
        def python_shell():
            self.engine.config['crash_on_boot'] = False
            if self.config['runfile'] is not None:
                try:
                    pass
                    #run_file(self.config['runfile'])
                except Exception as e:
                    traceback.print_exc(e)
            shell = self.get_shell(self.config['shell'])

            shell(header=self.header)
        return python_shell


def main():
    engine = get_engine()
    vac_shell = VacShell()
    run(vac_shell.get_shell_func(), config=None)
    engine.perform_exit()


if __name__ == '__main__':
    main()

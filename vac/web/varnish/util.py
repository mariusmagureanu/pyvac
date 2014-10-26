__author__ = 'mariusmagureanu'
from twisted.internet import threads
from functools import wraps
from contextlib import contextmanager
import signal
import logging


log = logging.getLogger('vac')


def defer_to_thread(function):
    @wraps(function)
    def substitution_function(*args, **kwargs):
        return threads.deferToThread(function, *args, **kwargs)
    return substitution_function


@contextmanager
def restore_signal_handlers(*signal_names):
    """
    This contextmanager restores the signal handling callback
    that was registered (via. signal.signal(SIGCODE, callback))
    before the code in the with block was run.

    This contextmanager reattaches the original signal callback when
    running code that changes specific signals that
    we do not have control over, e.g.  reactor._handleSignals()
    """
    # Store the original callback for the signal_names on __enter__
    signal_handlers = {}
    for signal_name in signal_names:
        signal_code = getattr(signal, signal_name, None)
        if signal_code:
            signal_handlers[signal_code] = signal.getsignal(signal_code)
    try:
        # Code in the with block can change the signal callback:
        yield signal_handlers
    finally:
        # Restore the original callback for the signal on __exit__
        for signal_code, handler in signal_handlers.iteritems():
            signal.signal(signal_code, handler)

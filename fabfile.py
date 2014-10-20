from __future__ import with_statement
from fabric import colors
from fabric.api import *
import fabric.contrib.files
import os
import shlex
import commands
import subprocess

this_directory = os.path.dirname(os.path.abspath(__file__))

fab = 'fab'
# FIXME: on Fedora, pip is pip-python
pip = 'pip'
nosetests = 'nosetests'


def clean_pyc():
    """
    Removes all *.pyc files.
    """
    print 'Number of .pyc files we found was: %s' % local(
        "find . -iname '*.pyc' | wc -l")
    local("find . -iname '*.pyc' -delete", capture=False)
    local("find . -name 'tnglogs' -prune -exec rm -r '{}' \;", capture=False)
    local("find . -name '_trial_temp' -prune -exec rm -r '{}' \;",
          capture=False)


def clean_boring():
    print "Number of ~ files we found was: %s" % local(
        "find . -iname '*~' | wc -l")
    local("find . -iname '*~' -delete", capture=False)


def install(extras=None):
    """
    Installs vac package. May require sudo.
    """
    if extras is None:
        extras = ""
    else:
        extras = "[%s]" % (extras,)

    local('%s install -e .%s' % (pip, extras), capture=False)


def dist_clean():
    """Intended to clean up artifacts from installing PyVac as root."""
    blacklist = ['docs',
                 'build',
                 'VAC.egg-info',
                 'TODO',
                 'DEV_INSTALL']
    with cd(os.getcwd()):
        for item in blacklist:
            local('sudo rm -rf %s' % item)


def pdf():
    """
    Generates documentation as pdf format.
    """
    usage_folder = os.path.join(this_directory, 'docs', 'usage')
    status, output = commands.getstatusoutput(
        'cd %s; pdflatex usage.tex' % usage_folder)
    if status != 0:
        print "===LATEX COMPILE FAILED===\n%s" % output
        return
    else:
        print "PDF Created: %s/usage.pdf" % usage_folder


def sphinx():
    """
    Generates documentation, default is html format.
    """
    sphinx_dir = os.path.join(this_directory, 'docs', 'sphinx')
    local('cd %s; make html' % sphinx_dir, capture=False)
    link = "file://" + os.path.join(sphinx_dir, '_build', 'html', 'index.html')
    print "Sphinx docs created: %s" % link


def clean_sphinx():
    """
    Cleans the output of the sphinx task.
    """
    sphinx_dir = os.path.join(this_directory, 'docs', 'sphinx')
    local('cd %s; make clean' % sphinx_dir, capture=False)


def test():
    """
    Runs unit-tests and checks .py files
    against PEP8 standard.
    """
    env = dict(os.environ)

    pep8 = subprocess.Popen(['pep8', '--config=pep8_config',
                             'vac', 'fabfile.py', 'setup.py'],
                            cwd=this_directory,
                            env=env,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    cmd_line = 'nosetests -v'
    p = subprocess.Popen(shlex.split(cmd_line),
                         cwd=this_directory,
                         env=env)
    pep8_std_out = pep8.stdout.read()
    ec = p.wait()
    pep8_ec = pep8.wait()
    if pep8_ec:
        print ' PEP8 '.center(80, '-')
        print colors.red(pep8_std_out)
        print '-' * 80
    if ec + pep8_ec != 0:
        pass_ = colors.green('Pass')
        fail_ = colors.red('Fail')

        test_str = pass_ if not ec else fail_
        pep8_str = pass_ if not pep8_ec else fail_

        fabric.utils.error("\nTests: {}\nPEP8: {}".format(test_str, pep8_str))


def tox_test():
    """
    Run tests in tox environment which should also ensure setup.py works
    :return:
    """
    local('tox --recreate')
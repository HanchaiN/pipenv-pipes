# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import sys
from subprocess import Popen, PIPE

from . import PipedPopen


def call_venv(project_dir, timeout=10):
    """ Calls ``pipenv --venv`` from a given project directory """
    output, code = PipedPopen(cmds=['pipenv', '--venv'], cwd=project_dir, timeout=timeout)
    return output, code


def call_shell(cwd, envname='pipenv-shell', timeout=None):
    """ Calls ``pipenv shell``` from a given envname """
    environ = dict(os.environ)
    environ['PROMPT'] = '({}){}'.format(envname, os.getenv('PROMPT', ''))

    is_test = 'PYTEST_CURRENT_TEST' in os.environ
    stdout = PIPE if is_test else sys.stdout
    stderr = PIPE if is_test else sys.stderr

    proc = Popen(
        ['pipenv', 'shell'],
        cwd=cwd,
        shell=False,
        stdout=stdout,
        stderr=stderr,
        env=environ,
        )
    out, err = proc.communicate(timeout=timeout)
    output = out or err
    code = proc.returncode
    return output, code, proc


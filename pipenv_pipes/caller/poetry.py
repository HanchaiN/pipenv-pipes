# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import sys
from subprocess import Popen, PIPE

from . import PipedPopen


def call_venv(project_dir, timeout=10):
    """ Calls ``poetry list`` from a given project directory """
    output, code = PipedPopen(cmds=['poetry', 'env', 'info', '-p'], cwd=project_dir, timeout=timeout)
    return output, code


def call_shell(cwd, envname='poetry-shell', timeout=None):
    """ Calls ``poetry shell``` from a given envname """
    environ = dict(os.environ)
    try:
        from dotenv import dotenv_values

        dotenv = dotenv_values(os.path.join(cwd, '.env'))
        environ.update(dotenv)
    except ImportError:
        pass
    environ['PROMPT'] = '({}){}'.format(envname, environ.get('PROMPT', ''))
    shell = environ.get('SHELL')

    is_test = 'PYTEST_CURRENT_TEST' in os.environ
    stdout = PIPE if is_test else sys.stdout
    stderr = PIPE if is_test else sys.stderr

    proc = Popen(
        ['poetry', 'run', shell] if shell is not None else ['poetry', 'shell'],
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

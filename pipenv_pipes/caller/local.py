# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import sys
from subprocess import Popen, PIPE

import click

from ..define import LOCAL_ENV, VenvType
from ..utils import check_local_venv_type

def _find_venv(project_dir):
    """ Find virtual environments from a given project directory """
    for folder_name in LOCAL_ENV:
        envpath = os.path.join(project_dir, folder_name)
        if not os.path.isdir(envpath):
            continue
        return envpath
    return None


def _call_venv(project_dir, timeout=10):
    """ List virtual environments from a given project directory """
    envpath = _find_venv(project_dir)
    if envpath is None:
        return 'No virtual environment found', 1
    return envpath, 0


def call_venv(project_dir, timeout=10):
    """ List virtual environments from a given project directory """
    venv_type = check_local_venv_type(project_dir)
    if venv_type == VenvType.LOCAL:
        return _call_venv(project_dir, timeout=timeout)
    if venv_type == VenvType.PIPENV:
        from .pipenv import call_venv as pipenv_call_venv

        return pipenv_call_venv(project_dir, timeout=timeout)
    if venv_type == VenvType.POETRY:
        from .poetry import call_venv as poetry_call_venv

        return poetry_call_venv(project_dir, timeout=timeout)
    return 'Unknown Venv Type', 1


def _find_activate(envpath):
    """ Finds the activation script in a given environment path """
    env_ls = os.listdir(envpath)
    if 'bin' in env_ls:
        binpath = os.path.join(envpath, 'bin', 'activate')
    elif 'Scripts' in env_ls:
        binpath = os.path.join(envpath, 'Scripts', 'activate')
    else:
        raise EnvironmentError(
            'could not find activation script path: {}'.format(envpath))
    if os.path.exists(binpath):
        return binpath
    else:
        raise EnvironmentError(
            'could not find activation script: {}'.format(envpath))


def _call_shell(cwd, envname='activated-shell', timeout=None):
    """ Calls shell with activated environment from a given envname """
    environ = dict(os.environ)
    try:
        from dotenv import dotenv_values

        dotenv = dotenv_values(os.path.join(cwd, '.env'))
        environ.update(dotenv)
    except ImportError:
        pass
    environ['PROMPT'] = '({}){}'.format(envname, environ.get('PROMPT', ''))
    shell = environ.get('SHELL', 'sh')
    envpath = _find_venv(cwd)
    if envpath is None:
        raise EnvironmentError('No virtual environment found')
    activate = _find_activate(envpath)
    activate = os.path.relpath(activate, cwd)


    is_test = 'PYTEST_CURRENT_TEST' in os.environ
    stdout = PIPE if is_test else sys.stdout
    stderr = PIPE if is_test else sys.stderr

    click.echo(click.style(f'Cannot activate environment `{activate}`, please run manually.', fg='yellow'))
    proc = Popen(
        [shell],
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


def call_shell(cwd, envname='activated-shell', timeout=None):
    """ Calls shell with activated environment from a given envname """
    venv_type = check_local_venv_type(cwd)
    if venv_type == VenvType.LOCAL:
        return _call_shell(cwd, envname=envname, timeout=timeout)
    if venv_type == VenvType.PIPENV:
        from .pipenv import call_shell as pipenv_call_shell

        return pipenv_call_shell(cwd, envname=envname, timeout=timeout)
    if venv_type == VenvType.POETRY:
        from .poetry import call_shell as poetry_call_shell

        return poetry_call_shell(cwd, envname=envname, timeout=timeout)
    return 'Unknown Venv Type', 1
# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
from subprocess import PIPE, Popen

from ..define import VenvType


def PipedPopen(cmds, **kwargs):
    """ Helper Piped Process for drier code"""
    timeout = kwargs.pop('timeout', None)
    env = kwargs.pop('env', dict(os.environ))
    proc = Popen(
        cmds,
        stdout=PIPE,
        stderr=PIPE,
        env=env,
        **kwargs
    )
    out, err = proc.communicate(timeout=timeout)
    output = out.decode().strip() or err.decode().strip()
    code = proc.returncode
    return output.strip(), code


def call_python_version(pybinpath):
    binpath = os.path.dirname(pybinpath)
    pybinpath = os.path.join(binpath, 'python')
    output, code = PipedPopen(cmds=[pybinpath, '--version'])
    return output, code


def call_venv(project_dir, venv_type, timeout=10):
    """ Calls ``pipenv --venv`` from a given project directory """
    if venv_type is None:
        for venv_type_ in VenvType:
            try:
                output, code = call_venv(project_dir, venv_type_)
            except FileNotFoundError:
                continue
            if code == 0:
                return output, code
        return 'no virtualenv has been created', 1
    if venv_type == VenvType.PIPENV:
        from .pipenv import call_venv as call_pipenv_venv

        return call_pipenv_venv(project_dir, timeout=timeout)
    if venv_type == VenvType.POETRY:
        from .poetry import call_venv as call_poetry_venv

        return call_poetry_venv(project_dir, timeout=timeout)
    if venv_type == VenvType.LOCAL:
        from .local import call_venv as call_local_venv

        return call_local_venv(project_dir, timeout=timeout)
    return f'Unknown Venv Type ({venv_type})', 1


def call_shell(cwd, venv_type, envname='pipenv-shell', timeout=None):
    """ Calls ``pipenv shell``` from a given envname """
    if venv_type == VenvType.PIPENV:
        from .pipenv import call_shell as call_pipenv_shell

        return call_pipenv_shell(cwd, envname=envname, timeout=timeout)
    if venv_type == VenvType.POETRY:
        from .poetry import call_shell as call_poetry_shell

        return call_poetry_shell(cwd, envname=envname, timeout=timeout)
    if venv_type == VenvType.LOCAL:
        from .local import call_shell as call_local_shell

        return call_local_shell(cwd, envname=envname, timeout=timeout)
    return f'Unknown Venv Type ({venv_type})', 1
# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

from collections import namedtuple
import enum



class VenvType(enum.Enum):
    LOCAL = 'local'
    PIPENV = 'pipenv'
    POETRY = 'poetry'


LOCAL_ENV = ('.venv', 'venv', 'env')
PIPENV_FOLDER_PAT = r'^(.+)-[\w_-]{8}$'
POETRY_FOLDER_PAT = r'^(.+)-[\w_-]{8}-[^-]+$'

venv_pattern = {
    VenvType.LOCAL: None,
    VenvType.PIPENV: PIPENV_FOLDER_PAT,
    VenvType.POETRY: POETRY_FOLDER_PAT,
}

Environment = namedtuple('Environment', [
    'envpath',
    'envname',
    'project_name',
    'binpath',
    'venv_type',
    ])
# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import re

from pipenv_pipes.define import VenvType

from .define import VenvType, venv_pattern
from .environment import EnvVars


def get_project_info(folder_name):
    """ Returns info of a project given a Pipenv Environment folder """
    for venv_type, pattern in venv_pattern.items():
        if pattern is None:
            continue
        match = re.search(pattern, folder_name)
        if match:
            return match.group(1), venv_type
    return None, None

def get_project_info_local(envpath):
    """ Returns info of a project given a Local Environment folder """
    project_name = os.path.basename(os.path.dirname(envpath))
    return project_name, VenvType.LOCAL

def get_query_matches(environments, query):
    """ Returns matching environments from an Environment list and a query """
    matches = []
    for environment in environments:
        if query.lower() in environment.envname.lower():
            matches.append(environment)
    return matches


def get_project_dir_filepath(envpath):
    """ Returns .project filepath from an environment path """
    return os.path.join(envpath, '.project')


def get_index_from_query(query):
    """ Index should be passed as 1: """
    pat = r'(\d+):$'
    match = re.match(pat, query)
    return None if not match else int(match.group(1))


def collapse_path(path):
    """ Replaces Home and WorkOn values in a path for their variable names """
    envvars = EnvVars()
    workon = envvars.PIPENV_HOME
    home = os.path.expanduser("~")
    path = path.replace(workon, '$PIPENV_HOME')
    path = path.replace(home, '~')
    return path


def any_file_exists(root, *files):
    """ Check if any of the files exist in the root """
    return any(os.path.isfile(os.path.join(root, f)) for f in files)


def check_local_venv_type(project_dir):
    """ Check venv manager from a given project directory """
    if any_file_exists(project_dir, 'Pipfile', 'Pipfile.lock'):
        return VenvType.PIPENV
    if any_file_exists(project_dir, 'poetry.toml', 'poetry.lock'):
        return VenvType.POETRY
    if any_file_exists(project_dir, 'pyproject.toml'):
        import tomllib

        with open(os.path.join(project_dir, 'pyproject.toml'), 'rb') as f:
            pyproject = tomllib.load(f)
        if 'tool' in pyproject and 'poetry' in pyproject['tool']:
            return VenvType.POETRY
    return VenvType.LOCAL

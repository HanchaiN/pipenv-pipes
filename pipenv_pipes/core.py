# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import shutil
import time

from .caller import call_python_version
from .define import LOCAL_ENV
from .define import Environment, VenvType
from .utils import (
    get_project_info,
    get_project_dir_filepath,
    get_project_info_local,
)


def find_environments(pipenv_home):
    """
    Returns Environment NamedTuple created from list of folders found in the
    Pipenv Environment location
    """
    environments = []
    cwd = os.getcwd()
    for folder_name in LOCAL_ENV:
        envpath = os.path.join(cwd, folder_name)
        if not os.path.isdir(envpath):
            continue
        project_name, venv_type = get_project_info_local(envpath)
        venv_type = VenvType.LOCAL
        envname = f"{project_name}/{folder_name}"

        binpath = find_binary(envpath)
        environment = Environment(project_name=project_name,
                                  envpath=envpath,
                                  envname=envname,
                                  binpath=binpath,
                                  venv_type=venv_type,
                                  )
        environments.append(environment)
        break
    for folder_name in sorted(os.listdir(pipenv_home)):
        envpath = os.path.join(pipenv_home, folder_name)
        project_name, venv_type = get_project_info(folder_name)
        if not project_name:
            continue

        binpath = find_binary(envpath)
        environment = Environment(project_name=project_name,
                                  envpath=envpath,
                                  envname=folder_name,
                                  binpath=binpath,
                                  venv_type=venv_type,
                                  )
        environments.append(environment)
    return environments


def find_binary(envpath):
    """ Finds the python binary in a given environment path """
    env_ls = os.listdir(envpath)
    if 'bin' in env_ls:
        binpath = os.path.join(envpath, 'bin', 'python')
    elif 'Scripts' in env_ls:
        binpath = os.path.join(envpath, 'Scripts', 'python.exe')
    else:
        raise EnvironmentError(
            'could not find python binary path: {}'.format(envpath))
    if os.path.exists(binpath):
        return binpath
    else:
        raise EnvironmentError(
            'could not find python binary: {}'.format(envpath))


def get_binary_version(envpath):
    """ Returns a string indicating the Python version (Python 3.5.6) """
    pybinpath = find_binary(envpath)
    output, code = call_python_version(pybinpath)
    if not code:
        return output
    else:
        raise EnvironmentError(
            'could not get binary version: {}'.format(output))


def delete_directory(envpath):
    """ Deletes the enviroment by its path """
    attempt = 0
    while attempt < 5:
        try:
            shutil.rmtree(envpath)
        except (FileNotFoundError, OSError):
            pass
        if not os.path.exists(envpath):
            return True
        attempt += 1
        time.sleep(0.25)


###############################
# Project Dir File (.project) #
###############################


def read_project_dir_file(envpath):
    project_file = get_project_dir_filepath(envpath)
    try:
        with open(project_file) as fp:
            return fp.read().strip()
    except IOError:
        return


def write_project_dir_project_file(envpath, project_dir):
    project_file = get_project_dir_filepath(envpath)
    with open(project_file, 'w') as fp:
        return fp.write(project_dir)


def delete_project_dir_file(envpath):
    project_file = get_project_dir_filepath(envpath)
    try:
        os.remove(project_file)
    except IOError:
        pass
    else:
        return project_file

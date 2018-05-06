import pytest  # noqa: F401
import os
from os.path import join

from pipenv_pipes.core import (
    find_environments,
    read_project_dir_file,
    write_project_dir_project_file,
    delete_project_dir_file,
)


class TestFindEnvironments():

    def test_find_environments(self, runner):
        with runner.isolated_filesystem():
            os.makedirs('proj1-12345678')
            os.makedirs('proj2-12345678')
            os.makedirs('nonenvfolder')
            environments = find_environments('.')
        assert len(environments) == 2
        assert 'proj1' in [e.project_name for e in environments]

    def test_find_environments_empty(self, temp_empty):
        """ Environment could be empty """
        environments = find_environments(temp_empty)
        assert len(environments) == 0

    def test_find_environments_does_not_exit(self):
        """ Invalid Folder. CLI Entry should catch, core func should fail """
        with pytest.raises(IOError):
            find_environments('/fakedir/')


class TestProjectDirFile():

    """ Test functions for managing the .project file, aka project_dir file """

    def test_write_project_dir_project_file(self, temp_empty):
        project_file = join(temp_empty, '.project')
        project_dir = 'fakeProjectPath'
        write_project_dir_project_file(
            envpath=temp_empty,
            project_dir=project_dir)
        with open(project_file, 'r') as fp:
            assert fp.read() == project_dir

    def test_read_project_dir_file(self, temp_empty):
        project_file = join(temp_empty, '.project')
        with open(project_file, 'w') as fp:
            fp.write('fakePath')
        assert read_project_dir_file(temp_empty) == 'fakePath'

    def test_delete_project_dir_file(self, temp_empty):
        project_file = join(temp_empty, '.project')

        with open(project_file, 'w') as fp:
            fp.write('fakePath')
        delete_project_dir_file(temp_empty)
        assert not os.path.exists(project_file)

import os
from os.path import abspath, dirname


def set_test_dir_to_root() -> None:
    dir = abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.chdir(dirname(dir))

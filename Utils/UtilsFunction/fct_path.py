# -*- coding: utf-8 -*-
import logging
import subprocess
import os
from subprocess import call, check_output
import shlex

def rename_directory(old_path, new_path, old_name, new_name):
    logging.debug('transform {} into {}'.format(old_name, new_name))

    create_directory_if_not_exists(new_path)

    cmd = 'mv {}{} {}{}'.format(old_path, old_name, new_path, new_name)

    try:
        out = call(shlex.split(cmd))
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))


def create_directory_if_not_exists(path):
    """Vérifie si un chemin existe et crée le répertoire s'il n'existe pas.
        """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory {path} was created.")

def check_file_path(file_path, verbose = False):
    """Checks if the path to the file exists.
    Returns True if the path exists and False otherwise.
    """
    if verbose:
        print('looking for {}'.format(file_path))
    if os.path.isfile(file_path):
        return True
    else:
        return False

def check_path_for_string(path, string):
    """Checks if a string exists in the name of a file in the path.
    Returns True if the file name contains the string and False otherwise.
    """
    files = os.listdir(path)
    for file in files:
        if string in file:
            return True
    return False

def check_filename_for_string(path, file, string):
    """Checks if a string exists in the file name "file.py" in the path "path".
    Returns True if the file name contains the string and False otherwise.
    """
    file_path = os.path.join(path, file)
    if os.path.isfile(file_path):
        if string in file_path:
            return True
    return False
# -*- coding: utf-8 -*-
import subprocess

# %% imports

import numpy as np
from subprocess import call, check_output
import shlex
import logging
import timeit

from Utils.Module.fct_path import create_directory_if_not_exists
from Utils.Module.fct_verbose import printv
import os
from matplotlib.pyplot import imread


def dos2unix(csv_name):
    start_time = timeit.default_timer()
    cmd = "dos2unix {}".format(csv_name)
    logging.info('{}'.format(cmd))
    try:
        out = call(shlex.split(cmd))
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    stop_time = timeit.default_timer()
    logging.info("dos2unix took {}".format(stop_time - start_time))


def get_scalar_csv_from_txt(txt_name, csv_name):
    logging.info('Transform scalar signal {}'.format(txt_name))

    start_time = timeit.default_timer()
    cmd = "cat {} | tr ',' '\\n' > {}".format(txt_name, csv_name)
    logging.info('{}'.format(cmd))
    try:
        subprocess.run(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    stop_time = timeit.default_timer()
    logging.info("transform csv took {}".format(stop_time - start_time))


def cut_scalar_txt(txt_name, db_txt_name, nb_line):
    logging.info('Cut {} of scalar signal {}'.format(nb_line, txt_name))

    start_time = timeit.default_timer()

    cmd = "head - n {} {} > {}".format(nb_line, txt_name, db_txt_name)
    logging.info('{}'.format(cmd))
    try:
        subprocess.run(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    stop_time = timeit.default_timer()
    logging.info("cut txt took {}".format(stop_time - start_time))


def get_scalar_from_ssh(ssh_client, ssh_path, name_signal_ssh, txt_name):
    logging.info('Fetching scalar signal {}'.format(txt_name))

    start_time = timeit.default_timer()
    cmd = 'rsync -av --progress {}:{}{} {}'.format(ssh_client, ssh_path, name_signal_ssh,
                                                             txt_name)
    logging.info('{}'.format(cmd))
    try:
        subprocess.run(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    stop_time = timeit.default_timer()
    logging.info("transfert from ssh client took {}".format(stop_time - start_time))


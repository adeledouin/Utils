import numpy as np
import logging

from Utils.Module.fct_numpy import *


def find_min_dt(t_e, t_synchro):
    dt = t_e - t_synchro
    logging.debug('dt = {}'.format(dt))
    if not dt[dt > 0].size == 0:
        which_pict = np.where(dt == np.min(dt[dt > 0]))[0]
        if which_pict.size > 1:
            logging.debug('more than one pict found : {}'.format(which_pict))
            logging.debug('at dt = {} for t_e = {} vs {}'.format(dt[which_pict],
                                                                   t_e,
                                                                   t_synchro[which_pict]))
            if is_all_equal(t_synchro[which_pict]):
                logging.debug('ok c est same yuv')
                which_pict = which_pict[-1]
            else:
                logging.warning('autre pb que same yuv => faut coder !!')
    else:
        which_pict = - 1  ## première pict est avant le batch loade

    return which_pict
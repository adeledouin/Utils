
import numpy as np
from tqdm import tqdm

# ---------------------------------------------------------------------------------------------------------------------#
class Moments():
    """Class for computing basic statistical properties of a given signal."""

    # ---------------------------------------------------------#
    def __init__(self, signal: np.ndarray, axis: int = None, nan: bool = False):
        """ Initialize a new instance of Stat class.
        :param signal: a numpy array containing the signal data.
        :param axis: the axis along which to compute statistics. Default is None.
        :param nan: flag indicating whether to compute statistics with NaN values. Default is False.
        """

        if not nan:
            self.min = np.min(signal)
            self.max = np.max(signal)
            self.mean = np.mean(signal, axis=axis)
            self.var = np.var(signal, axis=axis, ddof=1)
            self.maxlikelihood = np.var(signal, axis=axis)
            self.sigma = np.sqrt(self.var)
            self.m2 = np.mean(signal * signal, axis=axis) / (2 * self.mean)

        else:
            self.min = np.nanmin(signal)
            self.max = np.nanmax(signal)
            self.mean = np.nanmean(signal, axis=axis)
            self.var = np.nanvar(signal, axis=axis, ddof=1)
            self.maxlikelihood = np.nanvar(signal, axis=axis)
            self.sigma = np.sqrt(self.var)
            self.m2 = np.mean(signal * signal, axis=axis) / (2 * self.mean)


def stat_moments(signal: np.ndarray, axis: int = 1):
    """

    :param signal:
    :param axis: 0 for stats per time step, 1 for stats per cycle
    :return:
    :rtype:

    """

    if np.isnan(signal).any():
        print("Le tableau contient des NaN")
        isnan = True
    else:
        isnan = False

    if np.size(signal.shape) == 1:
        stat_signal = Moments(signal.reshape(signal.size), nan=isnan)

        stat = np.stack([stat_signal.mean, stat_signal.var, stat_signal.sigma])
        mean_stat = None

    elif np.size(signal.shape) == 2:
        stat_signal = Moments(signal, axis=axis, nan=isnan)

        stat = np.stack([stat_signal.mean, stat_signal.var, stat_signal.sigma], axis=1)
        mean_stat = np.nanmean([stat_signal.mean, stat_signal.var, stat_signal.sigma], axis=1)
    else:
        stat = None
        mean_stat = None

        print('signal shape > 3D not implemented')

    return stat, mean_stat


# ------------------------------------------
def correlations(signal, size_cut=None, step=None):
    idx_tau_size = size_cut if size_cut is not None else signal.size
    idx_tau_step = step if step is not None else 1
    idx_tau = np.arange(0, idx_tau_size, idx_tau_step).astype(int)
    c = np.zeros(idx_tau.size)
    c[0] = 0
    bla = 1
    for j in tqdm(idx_tau[1::]):
        c[bla] = 1 / 2 * np.mean((signal[j::] - signal[0:-j]) ** 2)
        bla = bla + 1

    R_0 = np.mean(signal ** 2)
    plateaux = np.mean(c[int(np.round(idx_tau_size / 3))::])
    Cf = c

    inv_Cf = -Cf + plateaux

    return Cf, inv_Cf, plateaux, R_0, idx_tau

import sys
import timeit
import logging

sys.path.append('../../../../../../')

from Utils.Module.TraitementSignal.FiltrageNonLineaire import *

class DenoiseProximal():
    """
    Classe qui permet de denoiser le signal

    """

    # ---------------------------------------------------------#
    def __init__(self):
        """The constructor for DenoiseProximal
        """

    # ------------------------------------------
    def __set_params__(self, p, q, normL, mu, l=10, iter=1000):

        # Computation : fourier, mu = 0 marche ok
        self.param = {'filter': 'gradient',
                      'computation': 'direct',
                      'p': p,
                      'q': q,
                      'lambda': l,
                      'iter': iter}
        self.param['normL'] = normL
        self.param['mu'] = mu

    # ------------------------------------------
    def __set_op__(self):

        self.op = {
            'direct': lambda x: opL_1D(x, self.param),
            'adjoint': lambda x: opLadj_1D(x, self.param)
        }

    # ------------------------------------------
    def __set_fidelity_params__(self):
        if self.param['p'] == 1:
            self.prox_fidelity = lambda y, data, tau: prox_L1(y - data, tau) + data
            self.objective_fidelity = lambda y, data: np.sum(np.abs(y - data))
        elif self.param['p'] == 2:
            self.param['mu'] = 1
            self.prox_fidelity = lambda y, data, tau: prox_L2(y - data, tau) + data
            self.objective_fidelity = lambda y, data: 0.5 * np.sum(np.abs(y - data) ** 2)

    # ------------------------------------------
    def __set_regularization_params__(self):

        if self.param['q'] == 1:
            self.prox_regularization = lambda y, tau: prox_L1(y, tau)
            self.objective_regularization = lambda y, tau: tau * np.sum(np.abs(y))
        elif self.param['q'] == 2:
            self.prox_regularization = lambda y, tau: prox_L2(y, tau)
            self.objective_regularization = lambda y, tau: tau * np.sum(np.abs(y) ** 2)

    # ------------------------------------------
    def denoise(self, f, p=2, q=2, normL=1, mu=2):

        self.__set_params__(p, q, normL, mu)
        self.__set_op__()
        self.__set_fidelity_params__()
        self.__set_regularization_params__()

        self.prox = {
            'fidelity': self.prox_fidelity,
            'regularization': self.prox_regularization
        }
        self.objective = {
            'fidelity': self.objective_fidelity,
            'regularization': self.objective_regularization
        }

        start_time = timeit.default_timer()
        x1, crit1 = PD_ChambollePock(f, self.param, self.op, self.prox, self.objective, epsilon=1e-6)
        stop_time = timeit.default_timer()
        logging.info("denoise {} pts took {}".format(f.size, stop_time - start_time))

        return x1, crit1
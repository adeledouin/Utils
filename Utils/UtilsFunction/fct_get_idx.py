import numpy as np
from scipy.sparse import csr_matrix


def np_where(arr, val):
    return np.where(arr == val)[0]


def get_indices_simple(data):
    return [np_where(data, i) for i in range(0, data.max() + 1)]


def compute_M(data):
    cols = np.arange(data.size)
    return csr_matrix((cols, (data.ravel(), cols)),
                      shape=(data.max() + 1, data.size))


def get_indices_sparse(data):
    M = compute_M(data)
    return [np.unravel_index(row.data, data.shape) for row in M]
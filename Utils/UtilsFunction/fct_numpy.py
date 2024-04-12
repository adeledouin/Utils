import logging

import numpy
import numpy as np
import logging

def find_intersect(arr1, arr2):
    # Trouver l'intersection entre arr1 et arr2
    intersection = np.intersect1d(arr1, arr2)
    return intersection

def is_subset(sub, arr):
    # Vérifier si tous les éléments de la plage sont présents dans a
    all_in_subset = np.all(np.isin(sub, arr))

    if all_in_subset:
        logging.debug("Tous les éléments de la plage sont présents dans a.")
    else:
        logging.debug("Certains éléments de la plage ne sont pas présents dans a.")

    return all_in_subset

def is_unique(arr):
    # Trouver les valeurs uniques dans le tableau
    unique_values = np.unique(arr)

    # Comparer la longueur du tableau d'origine avec le tableau unique
    if len(arr) == len(unique_values):
        unique = True
        logging.debug("Il n'y a pas de doublons dans le tableau.")
    else:
        logging.debug("Il y a des doublons dans le tableau.")
        unique = False

    return unique

def make_unique(arr):
    # Trouver les valeurs uniques dans le tableau
    unique_values = np.unique(arr)

    return unique_values

def find_duplicate(arr):
    # Trouver les valeurs uniques dans le tableau
    unique_values, unique_counts = np.unique(arr, return_counts=True)

    # Identifier les doublons
    duplicates = unique_values[unique_counts > 1]

    # Afficher les doublons
    logging.debug("Doublons dans le tableau :")
    where_duplicate = [0 for i in range(np.size(duplicates))]
    for i in range(np.size(duplicates)):
        where_duplicate[i] = np.where(arr == duplicates[i])[0]

    return where_duplicate


def is_sorted_ascending(arr):
    return np.all(arr[:-1] <= arr[1:])


def is_sorted_descending(arr):
    return np.all(arr[:-1] >= arr[1:])


def is_sorted(arr):
    return is_sorted_ascending(arr) or is_sorted_descending(arr)


def find_max_arr(arr):
    return np.where(arr == np.max(arr))[0]


def find_min_arr(arr):
    return np.where(arr == np.min(arr))[0]


def is_equal(arr1, arr2):
    return np.array_equal(arr1, arr2)


def is_all_equal(arr):
    # Vérifier si tous les éléments de `arr` sont égaux
    return np.all(arr == arr[0])


def is_alterne(sort_idx):
    should_be_up_idx = np.arange(0, sort_idx[0, :].size - 1)
    should_be_down_idx = np.arange(1, sort_idx[0, :].size)

    return (sort_idx[1, should_be_up_idx] + sort_idx[1, should_be_down_idx]).any() == 0


def is_equal_size(arr1, arr2):
    return np.size(arr1) == np.size(arr2)


def is_equal_shape(arr1, arr2):
    return np.shape(arr1) == np.shape(arr2)


def is_supp_arr(arr1, arr2):
    return np.all(arr2 - arr1 > 0)


def is_equal_value(val1, val2):
    return val1 == val2


def set_diff(arr1, arr2):
    # Trouver les éléments différents entre a et b
    return np.setdiff1d(arr1, arr2)


def create_chunk(chunk_size, arr=None):
    if arr is not None:
        # Découper l'array en chunks de taille maximale
        chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
    else:
        logging.warning('a coder')
        chunks = None
    return chunks


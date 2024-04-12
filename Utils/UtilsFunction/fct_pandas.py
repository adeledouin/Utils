# -*- coding: utf-8 -*-

import numpy as np
import itertools
from tqdm import tqdm
import pandas as pd
import sys
import logging


# ---------------------------------------------------------#
def dataframe_info(dataframe: pd.DataFrame):
    logging.info('---------- Dataframe INFO:')
    logging.info(pd.DataFrame({'Taille RAW': sys.getsizeof(dataframe),
                        'Type': dataframe.dtypes,
                        'Min': dataframe.min(),
                        'Max': dataframe.max(),
                        'Count': len(dataframe)}))

# ---------------------------------------------------------#
def dataframe_stats(dataframe: pd.DataFrame):
    logging.info('---------- Dataframe STATS:')
    logging.info(pd.DataFrame({'Min': dataframe.min(),
                        'Max': dataframe.max(),
                        'Mean': dataframe.mean(),
                        'Sdt': np.sqrt(dataframe.var()),
                        'Count': len(dataframe)}))


# ---------------------------------------------------------#
def pandas_pearson_correlation(column1, column2):
    return column1.corr(column2)


# ---------------------------------------------------------#
def pandas_covariance(column1, column2):
        return column1.cov(column2)


# ---------------------------------------------------------#
def dataframe_to_array(dataframe: pd.DataFrame, column_name: str):
    return dataframe[column_name].values

# ---------------------------------------------------------#
def dataframe_to_numpy(dataframe: pd.DataFrame):
    return dataframe.to_numpy()

# ---------------------------------------------------------#
def colomn_to_lines(dataframe: pd.DataFrame):
    return pd.concat([dataframe], ignore_index=True)

import pandas
import numpy

def verify_array(data):
    return isinstance(data, numpy.ndarray)

def verify_dataframe(data):
    return isinstance(data, pandas.core.frame.DataFrame) 

def verify_series(data):
    return isinstance(data, pandas.core.series.Series)

def verify_list(data):
    return isinstance(data, list)

def verify_str(data):
    return isinstance(data, str)

from .tools import (
    fetch_num_columns,
    fetch_array_dim
)

def verify_valid_ndim_text(data):
    if verify_dataframe(data):
        if fetch_num_columns != 1:
            raise ValueError(
                    f'Expected 1 column in pandas.core.DataFrame, got {fetch_num_columns(data)}'
                )
    elif verify_array(data):
        if fetch_array_dim(data) != 1:
            raise ValueError(
                    f'Expected dimension of numpy.ndarray to be 1, got {fetch_array_dim(data)}'
                )

def verify_valid_dtype_text(data):
    if verify_str(data) or \
       verify_series(data) or \
       verify_array(data) or \
       verify_dataframe(data) or \
       verify_list(data):
       return True
    else:
        raise ValueError(
                    f'The data should be of one of the following type - list / str / numpy.ndarray / pandas.core.DataFrame / pandas.core.Series.'
                )
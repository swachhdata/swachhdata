from .verify import (
    verify_dataframe,
    verify_series,
    verify_array,
    verify_list
)

def fetch_num_rows(data):
    if verify_dataframe(data) or verify_array(data) or verify_series(data):
        return data.shape[0]
    
    elif verify_list(data):
        return len(data)

def fetch_num_columns(data):
    if verify_dataframe(data) or verify_array(data):
        return data.shape[1]

def fetch_array_dim(data):
    if verify_array(data):
        return data.ndim
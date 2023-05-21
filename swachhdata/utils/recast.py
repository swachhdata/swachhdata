from .verify import (
    verify_array,
    verify_dataframe,
    verify_list,
    verify_series,
    verify_str
)

from .tools import (
    fetch_array_dim,
    fetch_num_columns
)

def recast_to_list(data):

    if verify_list(data):
        return data
    
    elif verify_str(data):
        return [data]
    
    elif verify_array(data):
        if fetch_array_dim(data) == 1:
            return data.tolist()
        else:
            raise ValueError(
                    f'Expected dimension of numpy.ndarray to be 1, got {fetch_array_dim(data)}'
                )
    
    elif verify_dataframe(data):
        if fetch_num_columns(data) == 1:
            return data.values.reshape(1, -1).tolist()[0]
        else:
            raise ValueError(
                    f'Expected 1 column in pandas.core.DataFrame, got {fetch_num_columns(data)}'
                )
        
    elif verify_series(data):
        return data.values.tolist()
    
    else:
        raise ValueError(
                    f'The data should be of one of the following type - list / str / numpy.ndarray / pandas.core.DataFrame / pandas.core.Series.'
                )
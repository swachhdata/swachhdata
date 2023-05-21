from ..utils.verify import (
    verify_valid_dtype_text,
    verify_valid_ndim_text
)

from ..utils.tools import (
    fetch_num_rows
)

from ..utils.probe import (
    probe_string_data
)

class BaseTextDatum:

    """
    Data formatter, converts heterogenous text data types to homogenous list of string(s).

    Parameters
    ----------
    data / X : pandas.core.frame.DataFrame / pandas.core.series.Series / numpy.ndarray

    """

    def __init__(self, text=None):
        
        dtype_check = verify_valid_dtype_text(text)
        ndim_check = verify_valid_ndim_text(text)

        self.__data = None
        self.data = text
    
    def __len__(self):
        return fetch_num_rows(self.__data)

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, text):
        self.__data = probe_string_data(text)
    
    def recast(self):
        self.__data = probe_string_data(self.__data)

class TextDatum(BaseTextDatum):

    def __init__(self, text):
        super().__init__(text)
    
    def __add__(self, other):
        data = self.data + other.data
        return TextDatum(data)
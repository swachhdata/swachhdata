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
        
        self._data = None
        self.id_text_datum = None

        if text is not None:
            dtype_check = verify_valid_dtype_text(text)
            ndim_check = verify_valid_ndim_text(text)
            self.data = text
    
    @property
    def ntext(self):
        return fetch_num_rows(self._data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, text):
        self._data = probe_string_data(text)


class TextDatum(BaseTextDatum):

    def __init__(self, text):
        super().__init__(text)
    
    def __str__(self):
        return str(self.data)
    
    def __len__(self):
        return self.ntext
    
    def __add__(self, other):
        data = self.data + other.data
        return TextDatum(data)
    
    def recast(self):
        self._data = probe_string_data(self._data)
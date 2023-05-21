import pandas
from ..compose.core import BaseTextDatum

class TextFormatter:
    """
    Base Data Formatter for all recasts in swachhdata.text module

    Accepted text input format:
        * string
        * list of string
        * pandas.core.series.Series
    """

    def __init__(self):
        
        self._dtype = None
        self._text = None
        self._count = None
    
    def __text_formatter(self):
        
        self._count = len(self._text)

        if self._dtype == pandas.core.series.Series:
            self._text = self._text.tolist()
            self._dtype = type(self._text)

        if self._dtype == str:
            self._count = len(self._text.split())
            self._dtype = type(self._text)

class BaseTextRecast(BaseTextDatum):

    def __init__(self):
        """
        Initialize
        """
    
    def setup(self, data):
        """
        Setup
        """
        if hasattr(data, '__base_text_datum'):
            self.__dict__.update(data.__dict__)
        else:
            self.data = data
    
    def recast(self):
        """
        Recast
        """
    
    def setup_recast(self):
        """
        Setup & Recast
        """
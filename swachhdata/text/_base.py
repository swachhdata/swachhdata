import pandas
from ..compose.core import BaseTextDatum
from ..utils.exceptions import (
    IncorrectProcessDataType,
    IncorrectVerboseDataType,
    SetupNotImplementedError
)

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

    def __init__(self, process=None, verbose=0):
        """
        Initialize
        """
        if process is not None and not isinstance(process, str):
            raise IncorrectProcessDataType(process)
        
        if not isinstance(verbose, int):
            raise IncorrectVerboseDataType(verbose)
        
        self._setup_check = False
        self._process = process
        self._verbose_status = True
        self._verbose = verbose
        if self._verbose == -1:
            self._verbose_status = False
    
    def setup(self, text):
        """
        Setup
        """
        if hasattr(text, 'id_text_datum'):
            self.__dict__.update(text.__dict__)
        else:
            self.data = text
        
        self._setup_check = True
    
    def recast(self):
        """
        Recast
        """
        if not self._setup_check:
            raise SetupNotImplementedError(self._setup_check)

    def setup_recast(self, text=None):
        """
        Setup & Recast
        """
        if not self._setup_check:
            self.setup(text)
            return self.recast()
        else:
            return self.recast()

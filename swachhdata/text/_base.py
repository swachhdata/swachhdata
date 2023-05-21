import pandas

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
from ..compose.core import BaseTextDatum
from ..utils.exceptions import (
    IncorrectProcessDataType,
    IncorrectVerboseDataType,
    SetupNotImplementedError
)

class BaseTextRecast(BaseTextDatum):

    def __init__(self, process=None, verbose=0):
        """
        Initialize
        """
        super().__init__()
        if process is not None and not isinstance(process, str):
            raise IncorrectProcessDataType(process)
        
        if not isinstance(verbose, int):
            raise IncorrectVerboseDataType(verbose)
        
        self._setup_check = False
        self._process = process
        if verbose == -1:
            self._verbose_status = False
        else:
            self._verbose_status = True
        self._verbose = not bool(verbose)
    
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

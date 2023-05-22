from ..compose.core import BaseTextDatum
from ..utils.exceptions import (
    IncorrectProcessDataType,
    IncorrectVerboseDataType,
    SetupNotImplementedError
)

class ModuleTextRecast(BaseTextDatum):

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
        self.id_base_recast = None
    
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

from .pipeline import Pipeline

class BaseTextRecast(ModuleTextRecast):

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
        self.id_base_recast = None
    
    def __add__(self, other):

        if hasattr(self, 'id_pipeline') and hasattr(other, 'id_pipeline'):
            chain = self.chain + other.chain
        elif hasattr(self, 'id_pipeline') and not hasattr(other, 'id_pipeline'):
            chain = self.chain + [other]
        elif not hasattr(self, 'id_pipeline') and hasattr(other, 'id_pipeline'):
            chain = other.chain + [self]
        elif not hasattr(self, 'id_pipeline') and not hasattr(other, 'id_pipeline'):
            chain = [self] + [other]
        return Pipeline(chain)

    def __sub__(self, other):
        
        if hasattr(self, 'id_pipeline') and hasattr(other, 'id_base_recast'):
            if other in self.chain:
                self.chain.remove(other)
            else:
                raise ValueError(
                    f'{other} not found in Pipeline.chain'
                )
        return Pipeline(self.chain)
    
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

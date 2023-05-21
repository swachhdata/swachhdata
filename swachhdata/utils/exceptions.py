class IncorrectProcessDataType(Exception):
    """
    Raised when the process parameter is not of type <class 'str'>

    Args:
        process: str
        Exception (Exception): IncorrectProcessDataType
    """
    def __init__(self, process):
        self.message = f'Expected process input type <class \'str\'>, input type received {type(process)}'
        super().__init__(self.message)

class IncorrectVerboseDataType(Exception):
    """
    Raised when the verbose parameter is not of type <class 'int'>

    Args:
        verbose: int
        Exception (Exception): IncorrectVerboseDataType
    """
    def __init__(self, verbose):
        self.message = f'Expected verbose input type <class \'int\'>, input type received {type(verbose)}'
        super().__init__(self.message)

class SetupNotImplementedError(Exception):
    """
    Raised when the method recast is called before setup

    Args:
        Exception (Exception): SetupNotImplementedError
    """
    def __init__(self, verbose):
        self.message = f'method setup needs to be called before recast'
        super().__init__(self.message)
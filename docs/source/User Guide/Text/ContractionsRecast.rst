ContractionsRecast
==================

Recast text data by expanding Contractions
    
    Parameters
    ----------
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> # process='remove'
    >>> from swachhdata.text import ContractionsRecast
    >>> text = 'They're going to wildlife sanctuary, I guess Jon's going to be there too.'
    >>> rec = ContractionsRecast()
    >>> rec.setup(text)
    >>> rec.recast()
    'They are going to wildlife sanctuary, I guess Jon is going to be there too.'
    >>> # OR
    >>> rec.setup_recast(text)
    'They are going to wildlife sanctuary, I guess Jon is going to be there too.'
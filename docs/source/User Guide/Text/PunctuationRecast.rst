PunctuationRecast
=================

Recast text data by removing punctuations.
    
    Parameters
    ----------
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> from swachhdata.text import PunctuationRecast
    >>> text = 'Have you fed that dog? I told you, "Don't feed that dog!"'
    >>> rec = PunctuationRecast()
    >>> rec.setup(text)
    >>> rec.recast()
    'Have you fed that dog I told you Don t feed that dog'
    >>> # OR
    >>> rec.setup_recast(text)
    'Have you fed that dog I told you Don t feed that dog'
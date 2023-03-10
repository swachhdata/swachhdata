ShortWordsRecast
================

Recast text data by removing (short) words of specified length.
    
    Parameters
    ----------
    min_length int (>0), default=3
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> # min_length=3
    >>> from swachhdata.text import ShortWordsRecast
    >>> text = 'You can have a look at our catalogue in the services tab'
    >>> rec = ShortWordsRecast(min_length=3)
    >>> rec.setup(text)
    >>> rec.recast()
    'have look catalogue services'
    >>> # OR
    >>> rec.setup_recast(text)
    'have look catalogue services'
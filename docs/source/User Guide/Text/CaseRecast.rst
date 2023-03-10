CaseRecast
==========

Recast text data by case formatting the text

    Case formats supported:
        * UPPER case (upper)
        * lower case (lower)
        * First Upper case (fupper)
    
    Parameters
    ----------
    process: str ('lower', 'upper', 'fupper'), default='lower'
    verbose: int (0, 1, -1), default=0


    Examples
    --------
    >>> # process='lower'
    >>> from swachhdata.text import CaseRecast
    >>> text = 'You can have a look at our catalogue in the services tab'
    >>> rec = CaseRecast(process='lower')
    >>> rec.setup(text)
    >>> rec.recast()
    'you can have a look at our catalogue in the services tab'
    >>> # OR
    >>> rec.setup_recast(text)
    'you can have a look at our catalogue in the services tab'
    >>> 
    >>> # process='upper'
    >>> from swachhdata.text import CaseRecast
    >>> text = 'You can have a look at our catalogue in the services tab'
    >>> rec = CaseRecast(process='upper')
    >>> rec.setup(text)
    >>> rec.recast()
    'YOU CAN HAVE A LOOK AT OUR CATALOGUE IN THE SERVICES TAB'
    >>> # OR
    >>> rec.setup_recast(text)
    'YOU CAN HAVE A LOOK AT OUR CATALOGUE IN THE SERVICES TAB'
    >>> 
    >>> # process='fupper'
    >>> from swachhdata.text import CaseRecast
    >>> text = 'You can have a look at our catalogue in the services tab'
    >>> rec = CaseRecast(process='fupper')
    >>> rec.setup(text)
    >>> rec.recast()
    'You Can Have A Look At Our Catalogue In The Services Tab'
    >>> # OR
    >>> rec.setup_recast(text)
    'You Can Have A Look At Our Catalogue In The Services Tab'
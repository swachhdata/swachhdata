StemmingRecast
==============

Recast text data by performing stemming on it.
    
    Parameters
    ----------
    package: string ('nltk', 'extract', 'extract_remove'), default='nltk'
    method: string ('porter', 'snowball')
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> # method='porter'
    >>> from swachhdata.text import StemmingRecast
    >>> text = 'You can have a look at our catalogue at www.samplewebsite.com in the services tab'
    >>> rec = StemmingRecast(method='porter')
    >>> rec.setup(text)
    >>> rec.recast()
    'you can have a look at our catalogu at www.samplewebsite.com in the servic tab'
    >>> # OR
    >>> rec.setup_recast(text)
    'you can have a look at our catalogu at www.samplewebsite.com in the servic tab'
    >>> 
    >>> # method='snowball'
    >>> from swachhdata.text import StemmingRecast
    >>> text = 'You can have a look at our catalogue at www.samplewebsite.com in the services tab'
    >>> rec = StemmingRecast(method='snowball')
    >>> rec.setup(text)
    >>> rec.recast()
    'you can have a look at our catalogu at www.samplewebsite.com in the servic tab'
    >>> # OR
    >>> rec.setup_recast(text)
    'you can have a look at our catalogu at www.samplewebsite.com in the servic tab'
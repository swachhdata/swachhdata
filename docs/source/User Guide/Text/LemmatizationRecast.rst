LemmatizationRecast
===================

Recast text data by performing lemmatization on it.
    
    Parameters
    ----------
    package: string ('nltk', 'spacy'), default='nltk'
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> from swachhdata.text import LemmatizationRecast
    >>> text = 'You can have a look at our catalogue at www.samplewebsite.com in the services tab'
    >>> rec = LemmatizationRecast()
    >>> rec.setup(text)
    >>> rec.recast()
    'You can have a look at our catalogue at www.samplewebsite.com in the service tab'
    >>> # OR
    >>> rec.setup_recast(text)
    'You can have a look at our catalogue at www.samplewebsite.com in the service tab'
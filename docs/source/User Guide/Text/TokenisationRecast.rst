TokenisationRecast
==================

Recast text data by tokenising it.

    Tokenisation supported:
        * word tokenisation
        * sentence tokenisation
    
    Parameters
    ----------
    package: string ('nltk', 'spacy'), default='nltk'
    method: string ('word', 'sentence'), default=None
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> # method='word'
    >>> from swachhdata.text import TokenisationRecast
    >>> text = 'Grabbing her umbrella, Kate raced out of the house. Confused by her sister’s sudden change in mood, Jill stayed quiet.'
    >>> rec = TokenisationRecast(package='nltk', method='word')
    >>> rec.setup(text)
    >>> rec.recast()
    ['Grabbing', 'her', 'umbrella', ',', 'Kate', 'raced', 'out', 'of', 'the', 'house', '.', 'Confused', 'by', 'her', 'sister', '’', 's', 'sudden', 'change', 'in', 'mood', ',', 'Jill', 'stayed', 'quiet', '.']
    >>> # OR
    >>> rec.setup_recast(text)
    ['Grabbing', 'her', 'umbrella', ',', 'Kate', 'raced', 'out', 'of', 'the', 'house', '.', 'Confused', 'by', 'her', 'sister', '’', 's', 'sudden', 'change', 'in', 'mood', ',', 'Jill', 'stayed', 'quiet', '.']
    >>> 
    >>> # method='sentence'
    >>> from swachhdata.text import TokenisationRecast
    >>> text = 'You can have a look at our catalogue at www.samplewebsite.com in the services tab'
    >>> rec = TokenisationRecast(package='nltk', method='sentence')
    >>> rec.setup(text)
    >>> rec.recast()
    ['Grabbing her umbrella, Kate raced out of the house.', 'Confused by her sister’s sudden change in mood, Jill stayed quiet.']
    >>> # OR
    >>> rec.setup_recast(text)
    ['Grabbing her umbrella, Kate raced out of the house.', 'Confused by her sister’s sudden change in mood, Jill stayed quiet.']
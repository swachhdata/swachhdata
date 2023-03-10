StopWordsRecast
===============

Recast text data by removing stop words.
    
    Parameters
    ----------
     package : str ('nltk', 'spacy', 'gensim', 'custom'), default='nltk'
     stopwords : list (package='custom'), list of stopwords 
     verbose : int (0, 1, -1), default=0


    Examples
    --------
    >>> from swachhdata.text import StopWordsRecast
    >>> text = 'You can have a look at our catalogue in the services tab'
    >>> rec = StopWordsRecast(package='nltk')
    >>> rec.setup(text)
    >>> rec.recast()
    'You look catalogue services tab'
    >>> # OR
    >>> rec.setup_recast(text)
    'You look catalogue services tab'
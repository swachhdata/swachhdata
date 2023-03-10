MentionRecast
=============

Recast text data by removing or extracting Mentions.

    Mentions supported:
        * @jon_doe
        * @123jon_doe
        * @jon_doe123
        * @jondoe
        * @jon.doe
        * @jon:doe
        * @jon-doe
    
    Parameters
    ----------
    process: string ('remove', 'extract', 'extract_remove'), default='remove'
    verbose: int (0, 1, -1), default=0

    Attributes
    ----------
    get_regex_ : string
        regex being used by recast

    mention_ : list of string(s)
        extracted mention(s)
    

    Examples
    --------
    >>> # process='remove'
    >>> from swachhdata.text import MentionRecast
    >>> text = 'If you like the service we offer, post a review on google and tag us @jondoe'
    >>> rec = MentionRecast(process='remove')
    >>> rec.setup(text)
    >>> rec.recast()
    'If you like the service we offer, post a review on google and tag us'
    >>> # OR
    >>> rec.setup_recast(text)
    'If you like the service we offer, post a review on google and tag us'
    >>> 
    >>> # process='extract'
    >>> from swachhdata.text import MentionRecast
    >>> text = 'If you like the service we offer, post a review on google and tag us @jondoe'
    >>> rec = MentionRecast(process='extract')
    >>> rec.setup(text)
    >>> rec.recast()
    ['@jondoe']
    >>> # OR
    >>> rec.setup_recast(text)
    ['@jondoe']
    >>> 
    >>> # process='extract_remove'
    >>> from swachhdata.text import MentionRecast
    >>> text = 'If you like the service we offer, post a review on google and tag us @jondoe'
    >>> rec = MentionRecast(process='extract_remove')
    >>> rec.setup(text)
    >>> rec.recast()
    'If you like the service we offer, post a review on google and tag us'
    ['@jondoe']
    >>> # OR
    >>> rec.setup_recast(text)
    'If you like the service we offer, post a review on google and tag us'
    ['@jondoe']
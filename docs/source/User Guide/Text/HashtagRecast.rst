HashtagRecast
=============

Recast text data by removing or extracting Hashtag(s).

    Hashtags supported:
        * #sample_website
        * #sample_website123
        * #123sample_website
        * #sample_website
    
    Parameters
    ----------
    process: string ('remove', 'extract', 'extract_remove'), default='remove'
    verbose: int (0, 1, -1), default=0

    Attributes
    ----------
    get_regex_ : string
        regex being used by recast

    hashtag_ : list of string(s)
        extracted hashtag(s)
    

    Examples
    --------
    >>> # process='remove'
    >>> from swachhdata.text import HashtagRecast
    >>> text = 'Post a photo with tag #samplephoto to win prizes'
    >>> rec = HashtagRecast(process='remove')
    >>> rec.setup(text)
    >>> rec.recast()
    'Post a photo with tag to win prizes'
    >>> # OR
    >>> rec.setup_recast(text)
    'Post a photo with tag to win prizes'
    >>> 
    >>> # process='extract'
    >>> from swachhdata.text import HashtagRecast
    >>> text = 'Post a photo with tag #samplephoto to win prizes'
    >>> rec = HashtagRecast(process='extract')
    >>> rec.setup(text)
    >>> rec.recast()
    ['#samplephoto']
    >>> # OR
    >>> rec.setup_recast(text)
    ['#samplephoto']
    >>> 
    >>> # process='extract_remove'
    >>> from swachhdata.text import HashtagRecast
    >>> text = 'Post a photo with tag #samplephoto to win prizes'
    >>> rec = HashtagRecast(process='extract_remove')
    >>> rec.setup(text)
    >>> rec.recast()
    'Post a photo with tag to win prizes'
    ['#samplephoto']
    >>> # OR
    >>> rec.setup_recast(text)
    'Post a photo with tag to win prizes'
    ['#samplephoto']
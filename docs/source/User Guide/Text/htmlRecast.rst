htmlRecast
==========

Recast text data by removing HTML tags.

    uses lxml from BeautifulSoup to clean up html tags
    
    Parameters
    ----------
    verbose: int (0, 1, -1), default=0
    
    
    Examples
    --------
    >>> from swachhdata.text import htmlRecast
    >>> text = '<a href="www.samplewebsite.com">Click Here</a> to have a look at the menu in the services tab'
    >>> rec = htmlRecast()
    >>> rec.setup(text)
    >>> rec.recast()
    'Click Here to have a look at the menu in the services tab'
    >>> # OR
    >>> rec.setup_recast(text)
    'Click Here to have a look at the menu in the services tab'
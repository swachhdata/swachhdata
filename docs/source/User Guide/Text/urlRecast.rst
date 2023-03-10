urlRecast
=========

Recast text data by removing or extracting URLs.

    URLs supported:
        * HTTP address: http://www.website.com
        * HTTPS address: https://www.website.com
        * www.website.com
        * website.com
        * www.website.gov.in/website.html
        * IPv4 address: http://192.168.1.1/website.jpg
        * Address with different Port: www.website.com:8080/website.jpg
        * IPv4: 192.168.1.1/website.jpg
        * Ipv6: 2001:0db8:0000:85a3:0000:0000:ac1f:8001/website.jpg
        * Other permutations and combinations of above URLs.
    
    Parameters
    ----------
    process: string ('remove', 'extract', 'extract_remove'), default='remove'
    verbose: int (0, 1, -1), default=0

    Attributes
    ----------
     get_regex_ : string
        regex being used by recast

     url_ : list of string(s)
        extracted url(s)
    

    Examples
    --------
    >>> # process='remove'
    >>> from swachhdata.text import urlRecast
    >>> text = 'You can have a look at our catalogue at www.samplewebsite.com in the services tab'
    >>> url = urlRecast(process='remove')
    >>> url.setup(text)
    >>> url.recast()
    'You can have a look at our catalogue at in the services tab'
    >>> # OR
    >>> url.setup_recast(text)
    'You can have a look at our catalogue at in the services tab'
    >>> 
    >>> # process='extract'
    >>> from swachhdata.text import urlRecast
    >>> text = 'You can have a look at our catalogue at www.samplewebsite.com in the services tab'
    >>> url = urlRecast(process='extract')
    >>> url.setup(text)
    >>> url.recast()
    ['www.samplewebsite.com']
    >>> # OR
    >>> url.setup_recast(text)
    ['www.samplewebsite.com']
    >>> 
    >>> # process='extract_remove'
    >>> from swachhdata.text import urlRecast
    >>> text = 'You can have a look at our catalogue at www.samplewebsite.com in the services tab'
    >>> url = urlRecast(process='extract_remove')
    >>> url.setup(text)
    >>> url.recast()
    'You can have a look at our catalogue at in the services tab'
    ['www.samplewebsite.com']
    >>> # OR
    >>> url.setup_recast(text)
    'You can have a look at our catalogue at in the services tab'
    ['www.samplewebsite.com']
    >>>
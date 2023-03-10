NumberRecast
============

Recast text data by removing, replacing or extracting numbers.

    Number formats supported:
    * 1234567
    * 1,234,567 (use seperator=',')
    * 12,34,567 (use seperator=',')
    * 123.4567 (if not decimal, use seperator='.')
    
    Parameters
    ----------
    process: string ('remove', 'replace', 'extract', 'extract_remove', 'extract_replace'), default='remove'
    seperator = str (',', '.'), default=None
    verbose: int (0, 1, -1), default=0

    Attributes
    ----------
    number_ : list of number(s)
        extracted number(s)
    

    Examples
    --------
    >>> # process='remove'
    >>> from swachhdata.text import NumberRecast
    >>> text = 'The sales turnover of quarter 1 this year was $ 123456'
    >>> rec = NumberRecast(process='remove')
    >>> rec.setup(text)
    >>> rec.recast()
    'The sales turnover of quarter  this year was $ '
    >>> # OR
    >>> rec.setup_recast(text)
    'The sales turnover of quarter  this year was $ '
    >>> 
    >>> # process='replace'
    >>> from swachhdata.text import NumberRecast
    >>> text = 'The sales turnover of quarter 1 this year was $ 123456'
    >>> rec = NumberRecast(process='replace')
    >>> rec.setup(text)
    >>> rec.recast()
    'The sales turnover of quarter one this year was $ one hundred and twenty-three thousand, four hundred and fifty-six'
    >>> # OR
    >>> rec.setup_recast(text)
    'The sales turnover of quarter one this year was $ one hundred and twenty-three thousand, four hundred and fifty-six'
    >>> 
    >>> # process='extract'
    >>> from swachhdata.text import NumberRecast
    >>> text = 'The sales turnover of quarter 1 this year was $ 123456'
    >>> rec = NumberRecast(process='extract')
    >>> rec.setup(text)
    >>> rec.recast()
    ['1', '123456']
    >>> # OR
    >>> rec.setup_recast(text)
    ['1', '123456']
    >>> # process='extract_remove'
    >>> from swachhdata.text import NumberRecast
    >>> text = 'The sales turnover of quarter 1 this year was $ 123456'
    >>> rec = NumberRecast(process='extract_remove')
    >>> rec.setup(text)
    >>> rec.recast()
    'The sales turnover of quarter  this year was $ '
    ['1', '123456']
    >>> # OR
    >>> rec.setup_recast(text)
    'The sales turnover of quarter  this year was $ '
    ['1', '123456']
    >>> # process='extract_replace'
    >>> from swachhdata.text import NumberRecast
    >>> text = 'The sales turnover of quarter 1 this year was $ 123456'
    >>> rec = NumberRecast(process='extract_replace')
    >>> rec.setup(text)
    >>> rec.recast()
    'The sales turnover of quarter one this year was $ one hundred and twenty-three thousand, four hundred and fifty-six'
    ['1', '123456']
    >>> # OR
    >>> rec.setup_recast(text)
    'The sales turnover of quarter one this year was $ one hundred and twenty-three thousand, four hundred and fifty-six'
    ['1', '123456']
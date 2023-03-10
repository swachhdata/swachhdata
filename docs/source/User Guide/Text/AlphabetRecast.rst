AlphabetRecast
==============

Recast text data by removing all accented, non ascii characters and keeping only alphabets.
    
    Parameters
    ----------
    process: string / list ('all', 'keep_alpha', 'rem_non_ascii', 'rem_acc_char', or combination in a list), default='all'
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> # process='all' (default)
    >>> from swachhdata.text import AlphabetRecast
    >>> text = 'It was past lunch time so the 3 of us dropped by The Main Street Café ☕️ for a late lunch 🍛'
    >>> rec = AlphabetRecast()
    >>> rec.setup(text)
    >>> rec.recast()
    'It was past lunch time so the   of us dropped by The Main Street Cafe  for a late lunch '
    >>> # OR
    >>> rec.setup_recast(text
    'It was past lunch time so the   of us dropped by The Main Street Cafe  for a late lunch '
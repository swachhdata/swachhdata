EscapeSequenceRecast
====================

Recast text data by removing Escape Sequences.

    Parameters
    ----------
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> from swachhdata.text import EscapeSequenceRecast
    >>> text = 'To have a look at the menu\nClick Here'
    >>> rec = EscapeSequenceRecast()
    >>> rec.setup(text)
    >>> rec.recast()
    'To have a look at the menu Click Here'
    >>> # OR
    >>> rec.setup_recast(text)
    'To have a look at the menu Click Here'
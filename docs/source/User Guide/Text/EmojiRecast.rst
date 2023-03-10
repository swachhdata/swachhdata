EmojiRecast
===========

Recast text data by removing, replaing or extracting Emoji(s).
    
    Parameters
    ----------
    process: string ('remove', 'replace', 'extract', 'extract_remove', 'extract_replace'), default='remove'
    space_out = bool (True, False), default=False
    verbose: int (0, 1, -1), default=0

    Attributes
    ----------
    emoji_ : list of emoji(s)
        extracted emoji(s)
    

    Examples
    --------
    >>> # process='remove'
    >>> from swachhdata.text import EmojiRecast
    >>> text = 'Thanks a lot for your wishes! 😊'
    >>> rec = EmojiRecast(process='remove')
    >>> rec.setup(text)
    >>> rec.recast()
    'Thanks a lot for your wishes!'
    >>> # OR
    >>> rec.setup_recast(text)
    'Thanks a lot for your wishes!'
    >>> 
    >>> # process='replace'
    >>> from swachhdata.text import EmojiRecast
    >>> text = 'Thanks a lot for your wishes! 😊'
    >>> rec = EmojiRecast(process='replace')
    >>> rec.setup(text)
    >>> rec.recast()
    'Thanks a lot for your wishes! smiling_face_with_smiling_eyes '
    >>> # OR
    >>> rec.setup_recast(text)
    'Thanks a lot for your wishes! smiling_face_with_smiling_eyes '
    >>> 
    >>> # process='extract'
    >>> from swachhdata.text import EmojiRecast
    >>> text = 'Thanks a lot for your wishes! 😊'
    >>> rec = EmojiRecast(process='extract')
    >>> rec.setup(text)
    >>> rec.recast()
    ['😊']
    >>> # OR
    >>> rec.setup_recast(text)
    ['😊']
    >>> # process='extract_remove'
    >>> from swachhdata.text import EmojiRecast
    >>> text = 'Thanks a lot for your wishes! 😊'
    >>> rec = EmojiRecast(process='extract_remove')
    >>> rec.setup(text)
    >>> rec.recast()
    'Thanks a lot for your wishes!'
    ['😊']
    >>> # OR
    >>> rec.setup_recast(text)
    'Thanks a lot for your wishes!'
    ['😊']
    >>> # process='extract_replace'
    >>> from swachhdata.text import EmojiRecast
    >>> text = 'Thanks a lot for your wishes! 😊'
    >>> rec = EmojiRecast(process='extract_replace')
    >>> rec.setup(text)
    >>> rec.recast()
    'Thanks a lot for your wishes! smiling_face_with_smiling_eyes'
    ['😊']
    >>> # OR
    >>> rec.setup_recast(text)
    'Thanks a lot for your wishes! smiling_face_with_smiling_eyes'
    ['😊']
TextRecast
==========

TextRecast is a wrapper function for Recast classes.
    
      Parameters
      ----------
      text : string / list of strings / pandas.core.series.Series
      `**kwargs`

      Attributes
      ----------
      * url
      * mention
      * emoji
      * hashtag
      * token
      * number

      Returns
      -------
      ntext : string / list of strings
              Processed text

      kwargs Template
      ---------------

      >>> { urlRecast = {'process': 'extract_remove'},
      >>>   htmlRecast = True,
      >>>   EscapeSequenceRecast = True,
      >>>   MentionRecast = {'process': 'extract_remove'},
      >>>   ContractionsRecast = True,
      >>>   CaseRecast = {'process': 'lower'},
      >>>   EmojiRecast = {'process': 'extract_remove', 'space_out': False},
      >>>   HashtagRecast = {'process': 'extract_remove'},
      >>>   ShortWordsRecast = {'min_length': 3},
      >>>   StopWordsRecast = {'package': 'nltk', 'space_out': None},
      >>>   NumberRecast = {'process': 'remove', 'seperator': None},
      >>>   AlphabetRecast = {'process': 'all'},
      >>>   PunctuationRecast = True,
      >>>   StemmingRecast = {'package': 'nltk', 'method': 'porter'},
      >>>   LemmatizationRecast = {'package':'nltk'},
      >>>   TokenisationRecast = {'package': 'nltk', 'method': 'sentence' }
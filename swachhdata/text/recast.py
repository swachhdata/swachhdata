import re

from bs4 import BeautifulSoup
from html import unescape

import contractions

import spacy
import nltk
nltk.download('popular', quiet=True)

import num2words
import unicodedata
import string

import emoji
from emoji import EMOJI_DATA

from tqdm.auto import tqdm

from .base import BaseTextRecast
from ..utils import probe_string_data

class urlRecast(BaseTextRecast):
    """Recast text data by removing or extracting URLs.

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
    """

    def __init__(self, process='remove', verbose=0):

        super().__init__(process, verbose)
        self.urls = None
        self.__regex = r'\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b'
        self._name = 'urlRecast'

    @property
    def regex(self):
        return self.__regex

    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string (process='remove')
            Processed text
        url : list of strings (process='extract')
            Extracted URL
        ntext, url : string, list of strings (process='extract_remove')
            Processed text, Extracted URL
        """

        if self._process == 'remove':
            text = re.sub(r'\.{3}', '', text)
            text = re.sub(self.__regex, '', text)
            return text

        elif self._process == 'extract':
            text = re.sub(r'\.{3}', '', text)
            url = re.findall(self.__regex, text)
            return url

        elif self._process in ['extract_remove', 'remove_extract']:
            text = re.sub(r'\.{3}', '', text)
            url = re.findall(self.__regex, text)
            text = re.sub(self.__regex, '', text)
            return text, url

    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings (process='remove')
            Processed text
        url : list of strings (process='extract')
            Extracted URLs
        ntext, url : string / list of strings (process='extract_remove')
        """
        super().recast()

        if self._process in ['remove', 'extract', 'extract_remove', 'remove_extract']:
            data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
            data_tqdm.set_postfix({'urlRecast process': self._process})

        if self._process in ['remove', 'extract']:
            recast_text = [self.__base_recast(text) for text in data_tqdm]
            if self._process == 'extract':
                self.urls = recast_text
            else:
                self.data = recast_text
            return recast_text

        elif self._process in ['extract_remove', 'remove_extract']:
            recast_text, urls = [], []
            for text in data_tqdm:
                text, url = self.__base_recast(text)
                recast_text.append(text)
                urls.append(url)
            self.urls = urls
            self.data = recast_text
            return recast_text, urls

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings (process='remove')
            Processed text
        url : string / list of strings (process='extract')
            Extracted URLs
        ntext, url : string / list of strings, list of strings (process='extract_remove')
            Processed text, Extracted URLs
        """
        self.setup(text)
        return self.recast()



class htmlRecast(BaseTextRecast):
    """Recast text data by removing HTML tags.

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
    """

    def __init__(self, verbose=0):

        super().__init__(verbose=verbose)
        self._name = 'htmlRecast'
    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """
        soup = BeautifulSoup(unescape(text), 'lxml')
        text = soup.get_text()
        return text

    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings 
            Processed text
        """
        super().recast()

        data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
        data_tqdm.set_postfix({'htmlRecast process': 'remove'})
        recast_text = [self.__base_recast(text) for text in data_tqdm]
        self.data = recast_text
        return recast_text

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        self.setup(text)
        return self.recast()



class EscapeSequencesRecast(BaseTextRecast):
    """Recast text data by removing Escape Sequences.

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
    """


    def __init__(self, verbose=0):

        super().__init__(verbose=verbose)
        self._name = 'EscapeSequencesRecast'
    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """

        ntext = text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').replace('\n', ' ').replace('\f', ' ')
        return ntext

    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings 
            Processed text
        """
        super().recast()
        
        data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
        data_tqdm.set_postfix({'EscapeSequencesRecast process': 'remove'})
        recast_text = [self.__base_recast(text) for text in data_tqdm]
        self.data = recast_text
        return recast_text

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings (process='remove')
            Processed text
        """
        self.setup(text)
        return self.recast()



class MentionsRecast(BaseTextRecast):
    """Recast text data by removing or extracting Mentions.

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
    """

    def __init__(self, process='remove', verbose=0):

        super().__init__(process, verbose)
        self.__regex = '([@][A-Za-z0-9._:-]+)'
        self._name = 'MentionsRecast'

    @property
    def regex(self):
        return self.__regex
    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        text : string (process='remove')
            Processed text
        mention : list of strings (process='extract')
            Extracted Mention(s)
        text, mention : string, list of strings (process='extract_remove')
            Processed text, Extracted Mention(s)
        """
        if self._process == 'remove':
            return ' '.join(re.sub(self.__regex, ' ', text).split())

        elif self._process == 'extract':
            mention = re.findall(self.__regex, text)
            return mention

        elif self._process in ['extract_remove', 'remove_extract']:
            mention = re.findall(self.__regex, text)
            text = ' '.join(re.sub(self.__regex, ' ', text).split())
            return text, mention

    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        text : string / list of strings (process='remove')
            Processed text
        mention : list of strings (process='extract')
            Extracted Mention(s)
        text, mention : string / list of strings (process='extract_remove')
            Processed text, Extracted Mention(s)
        """
        super().recast()

        if self._process in ['remove', 'extract', 'extract_remove', 'remove_extract']:
            data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
            data_tqdm.set_postfix({'MentionRecast process': self._process})

        if self._process in ['remove', 'extract']:
            recast_text = [self.__base_recast(text) for text in data_tqdm]
            if self._process == 'extract':
                self.mentions = recast_text
            else:
                self.data = recast_text
            return recast_text

        elif self._process in ['extract_remove', 'remove_extract']:
            recast_text, mentions = [], []
            for text in data_tqdm:
                text, mention = self.__base_recast(text)
                recast_text.append(text)
                mentions.append(mention)
            self.mentions = mentions
            self.data = recast_text
            return recast_text, mentions

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        text : string / list of strings (process='remove')
            Processed text
        mentions : string / list of strings (process='extract')
            Extracted Mention(s)
        text, mentions : string / list of strings, list of strings (process='extract_remove')
            Processed text, Extracted Mention(s)
        """
        self.setup(text)
        return self.recast()



class ContractionsRecast(BaseTextRecast):
    """Recast text data by expanding Contractions
    
    Parameters
    ----------
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> # process='remove'
    >>> from swachhdata.text import ContractionsRecast
    >>> text = 'They're going to wildlife sanctuary, I guess Jon's going to be there too.'
    >>> rec = ContractionsRecast()
    >>> rec.setup(text)
    >>> rec.recast()
    'They are going to wildlife sanctuary, I guess Jon is going to be there too.'
    >>> # OR
    >>> rec.setup_recast(text)
    'They are going to wildlife sanctuary, I guess Jon is going to be there too.'
    """
    def __init__(self, verbose=0):

        super().__init__(verbose=verbose)
        self._name = 'ContractionsRecast'
    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        text : string
            Processed text
        """
        text = contractions.fix(text)
        return text

    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings 
            Processed text
        """
        super().recast()

        data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
        data_tqdm.set_postfix({'ContractionsRecast process': 'remove'})
        recast_text = [self.__base_recast(text) for text in data_tqdm]
        self.data = recast_text
        return recast_text

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings (process='remove')
            Processed text
        """
        self.setup(text)
        return self.recast()



class CaseRecast(BaseTextRecast):
    """Recast text data by case formatting the text

    Case formats supported:
        * UPPER case (upper)
        * lower case (lower)
        * Title (fupper / title / proper)
    
    Parameters
    ----------
    process: str ('lower', 'upper', 'fupper'), default='lower'
    verbose: int (0, 1, -1), default=0


    Examples
    --------
    >>> # process='lower'
    >>> from swachhdata.text import CaseRecast
    >>> text = 'You can have a look at our catalogue in the services tab'
    >>> rec = CaseRecast(process='lower')
    >>> rec.setup(text)
    >>> rec.recast()
    'you can have a look at our catalogue in the services tab'
    >>> # OR
    >>> rec.setup_recast(text)
    'you can have a look at our catalogue in the services tab'
    >>> 
    >>> # process='upper'
    >>> from swachhdata.text import CaseRecast
    >>> text = 'You can have a look at our catalogue in the services tab'
    >>> rec = CaseRecast(process='upper')
    >>> rec.setup(text)
    >>> rec.recast()
    'YOU CAN HAVE A LOOK AT OUR CATALOGUE IN THE SERVICES TAB'
    >>> # OR
    >>> rec.setup_recast(text)
    'YOU CAN HAVE A LOOK AT OUR CATALOGUE IN THE SERVICES TAB'
    >>> 
    >>> # process='fupper'
    >>> from swachhdata.text import CaseRecast
    >>> text = 'You can have a look at our catalogue in the services tab'
    >>> rec = CaseRecast(process='fupper')
    >>> rec.setup(text)
    >>> rec.recast()
    'You Can Have A Look At Our Catalogue In The Services Tab'
    >>> # OR
    >>> rec.setup_recast(text)
    'You Can Have A Look At Our Catalogue In The Services Tab'
    """

    def __init__(self, process='lower', verbose=0):

        super().__init__(process, verbose)
        self._name = 'CaseRecast'

    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        text : string (process='remove')
            Processed text
        rec : list of strings (process='extract')
            Extracted rec
        text, rec : string, list of strings (process='extract_remove')
            Processed text, Extracted rec
        """
        if self._process == 'lower':
            return text.lower()

        elif self._process == 'upper':
            return text.upper()
    
        elif self._process in ['fupper', 'title', 'proper']:
            return text.title()

    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        super().recast()

        data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
        data_tqdm.set_postfix({'CaseRecast process': self._process})
        recast_text = [self.__base_recast(text) for text in data_tqdm]
        self.data = recast_text
        return recast_text

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        self.setup(text)
        return self.recast()



class EmojiRecast(BaseTextRecast):
    """Recast text data by removing, replaing or extracting Emoji(s).
    
    Parameters
    ----------
    process: string ('remove', 'replace', 'extract', 'extract_remove', 'extract_replace'), default='remove'
    space_out = bool (True, False), default=False
    verbose: int (0, 1, -1), default=0

    Attributes
    ----------
    emoji : list of emoji(s)
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
    """

    def __init__(self, process='remove', space_out=False, verbose=0):

        super().__init__(process, verbose)
        self._space_out = space_out
        self.emojis = None
        self._emoji_list = list(EMOJI_DATA.keys())
        self._name = 'EmojiRecast'

    def __base_recast(self, text):
        """Perform selected process on the setup text

        Parameters
        ----------
        text : string / pandas.core.series.Series

        Returns
        -------
        ntext : string (process='remove' / process='replace')
            Processed text
        emoji : list of strings (process='extract')
            Extracted Emojis
        ntext, emoji : string, list of strings (process='extract_remove' / process='extract_replace')
            Processed text, Extracted Emojis
        """
        if self._space_out:
            spaced = ''
            for char in text:
                if char in self._emoji_list:
                    spaced += ' '
                spaced += char
            text = spaced
            text = re.sub(' +', ' ', text)
        
        if self._process == 'remove':
            allchars = [str for str in text]
            emoji_list = [c for c in allchars if c in self._emoji_list]
            text = ' '.join([str for str in text.split() if not any(j in str for j in emoji_list)])
            return text

        elif self._process == 'replace':
            text = emoji.demojize(text, delimiters=('', ''))
            return text

        elif self._process == 'extract':
            allchars = [str for str in text]
            emoji_list = [c for c in allchars if c in self._emoji_list]
            return emoji_list
        
        elif self._process in ['extract_remove', 'remove_extract']:
            allchars = [str for str in text]
            emoji_list = [c for c in allchars if c in self._emoji_list]
            text = ' '.join([str for str in text.split() if not any(j in str for j in emoji_list)])
            return text, emoji_list
        
        elif self._process in ['extract_replace', 'replace_extract']:
            allchars = [str for str in text]
            emoji_list = [c for c in allchars if c in self._emoji_list]
            text = emoji.demojize(text, delimiters=('', ''))
            return text, emoji_list

    def recast(self):
        """
        Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings (process='remove' / process='replace')
            Processed text
        emoji : string / list of strings (process='extract')
            Extracted Emojis
        ntext, emoji : string / list of strings, list of strings (process='extract_remove' / process='extract_replace')
            Processed text, Extracted Emojis
        """
        super().recast()

        if self._process in ['remove', 'extract', 'replace', 'extract_remove', 'remove_extract', 'extract_replace', 'replace_extract']:
            data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
            data_tqdm.set_postfix({'EmojiRecast process': self._process})

        if self._process in ['remove', 'extract', 'replace']:
            recast_text = [self.__base_recast(text) for text in data_tqdm]
            if self._process == 'extract':
                self.emojis = recast_text
            else:
                self.data = recast_text
            return recast_text

        elif self._process in ['extract_remove', 'remove_extract', 'extract_replace', 'replace_extract']:
            recast_text, emojis = [], []
            for text in data_tqdm:
                text, emoji = self.__base_recast(text)
                recast_text.append(text)
                emojis.append(emoji)
            self.emojis = emojis
            self.data = recast_text
            return recast_text, emojis

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings (process='remove' / process='replace')
            Processed text
        emoji : string / list of strings (process='extract')
            Extracted Emojis
        ntext, emoji : string / list of strings, list of strings (process='extract_remove' / process='extract_replace')
            Processed text, Extracted Emojis
        """
        self.setup(text)
        return self.recast()



class HashtagsRecast(BaseTextRecast):
    """Recast text data by removing or extracting Hashtag(s).

     supported:
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

    hashtags : list of string(s)
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
    """

    def __init__(self, process='remove', verbose=0):

        super().__init__(process, verbose)
        self.hashtags = None
        self.__regex = '([#][A-Za-z0-9_]+)'
        self._name = 'HashtagsRecast'
    
    @property
    def regex(self):
        return self.__regex
    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string (process='remove')
            Processed text
        hashtag : list of strings (process='extract')
            Extracted Hashtag(s)
        ntext, hashtag : string, list of strings (process='extract_remove')
            Processed text, Extracted Hashtag(s)
        """

        if self._process == 'remove':
            text = ' '.join(re.sub('([#][A-Za-z0-9_]+)', ' ', text).split())
            return text

        elif self._process == 'extract':
            hashtag = re.findall('([#][A-Za-z0-9_]+)', text)
            return hashtag

        elif self._process in ['extract_remove', 'remove_extract']:
            hashtag = re.findall('([#][A-Za-z0-9_]+)', text)
            text = ' '.join(re.sub('([#][A-Za-z0-9_]+)', ' ', text).split())
            return text, hashtag


    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings (process='remove')
            Processed text
        hashtag : list of strings (process='extract')
            Extracted Hashtag(s)
        ntext, hashtag : string / list of strings (process='extract_remove')
            Processed text, Extracted Hashtag(s)
        """
        super().recast()

        if self._process in ['remove', 'extract', 'extract_remove', 'remove_extract']:
            data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
            data_tqdm.set_postfix({'HashtagsRecast process': self._process})

        if self._process in ['remove', 'extract']:
            recast_text = [self.__base_recast(text) for text in data_tqdm]
            if self._process == 'extract':
                self.hashtags = recast_text
            else:
                self.data = recast_text
            return recast_text

        elif self._process in ['extract_remove', 'remove_extract']:
            recast_text, hashtags = [], []
            for text in data_tqdm:
                text, hashtag = self.__base_recast(text)
                recast_text.append(text)
                hashtags.append(hashtag)
            self.hashtags = hashtags
            self.data = recast_text
            return recast_text, hashtags

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings (process='remove')
            Processed text
        hashtag : string / list of strings (process='extract')
            Extracted Hashtag(s)
        ntext, hashtag : string / list of strings, list of strings (process='extract_remove')
            Processed text, Extracted Hashtag(s)
        """
        self.setup(text)
        return self.recast()



class ShortWordsRecast(BaseTextRecast):
    """Recast text data by removing (short) words of specified length.
    
    Parameters
    ----------
    min_length int (>0), default=3
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> # min_length=3
    >>> from swachhdata.text import ShortWordsRecast
    >>> text = 'You can have a look at our catalogue in the services tab'
    >>> rec = ShortWordsRecast(min_length=3)
    >>> rec.setup(text)
    >>> rec.recast()
    'have look catalogue services'
    >>> # OR
    >>> rec.setup_recast(text)
    'have look catalogue services'
    """

    def __init__(self, min_length=3, verbose=0):

        super().__init__(verbose=verbose)
        self._min_length = min_length
        self._name = 'ShortWordsRecast'

    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """
        ntext = [word for word in text.split() if len(word) > self._min_length]
        text = ' '.join(ntext)
        return text

    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings 
            Processed text
        """
        super().recast()
        data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
        data_tqdm.set_postfix({f'ShortWordsRecast [min_length = {self._min_length}] process': 'remove'})
        recast_text = [self.__base_recast(text) for text in data_tqdm]
        self.data = recast_text
        return recast_text

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """

        self.setup(text)
        return self.recast()



class StopWordsRecast(BaseTextRecast):
    """Recast text data by removing stop words.
    
    Parameters
    ----------
    package: str ('nltk', 'spacy', 'gensim', 'custom'), default='nltk'
    stopwords: list (package='custom'), list of stopwords 
    verbose: int (0, 1, -1), default=0


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
    """

    def __init__(self, package='nltk', stopwords=None, verbose=0):

        if package == 'custom':
            probe_string_data(stopwords)
        
        super().__init__(verbose=verbose)
        self._package = package
        self._stopWords = stopwords
        self._name = 'StopWordsRecast'
    
    def __setup_package(self):

        if self._package == 'nltk':
            from nltk.corpus import stopwords
            self._stopWords = set(stopwords.words('english'))

        elif self._package == 'spacy':
            sp = spacy.load('en_core_web_sm')
            self._stopWords = sp.Defaults.stop_words

    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """
        ntext = [word for word in text.split() if word not in self._stopWords]
        text = ' '.join(ntext)
        return text

    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        super().recast()
        self.__setup_package()

        data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
        data_tqdm.set_postfix({f'StopWordsRecast [package={self._package}] process': 'remove'})
        recast_text = [self.__base_recast(text) for text in data_tqdm]
        self.data = recast_text
        return recast_text

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        self.setup(text)
        return self.recast()



class NumbersRecast(BaseTextRecast):
    """Recast text data by removing, replacing or extracting numbers.

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
    numbers : list of number(s)
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
    """

    def __init__(self, process='remove', seperator=None, verbose=0):

        super().__init__(process, verbose)
        self._seperator = seperator
        self.numbers = None
        self._name = 'NumbersRecast'
    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string (process='remove' / process='replace')
            Processed text
        number : list of strings (process='extract')
            Extracted Number(s)
        ntext, number : string, list of strings (process='extract_remove' / process='extract_replace')
            Processed text, Extracted Number(s)
        """
        if self._seperator == ',':
            text = re.sub(r'(?<!\B)[,](?!\B)', '', text)
        
        elif self._seperator == '.':
            text = re.sub(r'(?<!\B)[.](?!\B)', '', text)
        
        if self._process == 'remove':
            return re.sub(r'[0-9]+', '', text, 0)

        elif self._process == 'replace':
            return re.sub(r'(\d+)', lambda x: num2words.num2words(int(x.group(0))), text, 0)

        elif self._process == 'extract':
            return re.findall(r'[0-9]+', text, 0)
        
        elif self._process in ['extract_remove', 'remove_extract']:
            numbers = re.findall(r'[0-9]+', text, 0)
            text = re.sub(r'[0-9]+', '', text, 0)
            return text, numbers
        
        elif self._process in ['extract_replace', 'replace_extract']:
            numbers = re.findall(r'[0-9]+', text, 0)
            text = re.sub(r'(\d+)', lambda x: num2words.num2words(int(x.group(0))), text, 0)
            return text, numbers


    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string (process='remove' / process='replace')
            Processed text
        number : list of strings (process='extract')
            Extracted Number(s)
        ntext, number : string, list of strings (process='extract_remove' / process='extract_replace')
            Processed text, Extracted Number(s)
        """
        super().recast()

        if self._process in ['remove', 'extract', 'replace', 'extract_remove', 'remove_extract', 'extract_replace', 'replace_extract']:
            data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
            data_tqdm.set_postfix({'NumberRecast process': self._process})

        if self._process in ['remove', 'extract', 'replace']:
            recast_text = [self.__base_recast(text) for text in data_tqdm]
            if self._process == 'extract':
                self.numbers = recast_text
            else:
                self.data = recast_text
            return recast_text

        elif self._process in ['extract_remove', 'remove_extract', 'extract_replace', 'replace_extract']:
            recast_text, numbers = [], []
            for text in data_tqdm:
                text, number = self.__base_recast(text)
                recast_text.append(text)
                numbers.append(number)
            self.numbers = numbers
            return recast_text, numbers

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string (process='remove' / process='replace')
            Processed text
        number : list of strings (process='extract')
            Extracted Number(s)
        ntext, number : string, list of strings (process='extract_remove' / process='extract_replace')
            Processed text, Extracted Number(s)
        """
        self.setup(text)
        return self.recast()



class AlphabetRecast(BaseTextRecast):
    """Recast text data by removing all accented, non ascii characters and keeping only alphabets.
    
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
    """

    def __init__(self, process='all', verbose=0):

        super().__init__(verbose=verbose)
        self._process = process
        self._name = 'AlphabetRecast'
    
    def __base_recast(self, text, process):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """

        if process == 'all':
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            text = re.sub(r'[^\x00-\x7F]+', ' ', text)
            text = re.sub(r'[^a-zA-Z]', ' ', text, 0)
            return text

        elif process == 'keep_alpha':
            return re.sub(r'[^a-zA-Z]', ' ', text, 0)

        elif process == 'rem_non_ascii':
            return re.sub(r'[^\x00-\x7F]+', ' ', text)

        elif process == 'rem_acc_char':
            return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')


    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        super().recast()
        
        text = self.data
        if isinstance(self._process, list):

            for process in self._process:
                data_tqdm = tqdm(text, leave=self._verbose_status, disable=self._verbose)
                data_tqdm.set_postfix({'AlphabetRecast process': f'{process}'})
                text = [self.__base_recast(text, process) for text in data_tqdm]
            
            self.data = text
            return text
        
        elif isinstance(self._process, str):

            data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
            data_tqdm.set_postfix({'AlphabetRecast process': f'{self._process}'})
            recast_text = [self.__base_recast(text, self._process) for text in data_tqdm]
            self.data = recast_text
            return recast_text

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        self.setup(text)
        return self.recast()



class PunctuationsRecast(BaseTextRecast):
    """Recast text data by removing punctuations.
    
    Parameters
    ----------
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> from swachhdata.text import PunctuationRecast
    >>> text = 'Have you fed that dog? I told you, "Don't feed that dog!"'
    >>> rec = PunctuationRecast()
    >>> rec.setup(text)
    >>> rec.recast()
    'Have you fed that dog I told you Don t feed that dog'
    >>> # OR
    >>> rec.setup_recast(text)
    'Have you fed that dog I told you Don t feed that dog'
    """

    def __init__(self, verbose=0):

        super().__init__(verbose=verbose)
        self._name = 'PunctuationsRecast'
    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """
        return text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).replace(' '*4, ' ').replace(' '*3, ' ').replace(' '*2, ' ').strip()

    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        super().recast()

        data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
        data_tqdm.set_postfix({'PunctuationRecast process': 'remove'})
        recast_text = [self.__base_recast(text) for text in data_tqdm]
        self.data = recast_text
        return recast_text

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        self.setup(text)
        return self.recast()



class TokenisationRecast(BaseTextRecast):
    """Recast text data by tokenising it.

    Tokenisation supported:
        * word tokenisation
        * sentence tokenisation
    
    Parameters
    ----------
    package: string ('nltk', 'spacy'), default='nltk'
    method: string ('word', 'sentence'), default=None
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> # method='word'
    >>> from swachhdata.text import TokenisationRecast
    >>> text = 'Grabbing her umbrella, Kate raced out of the house. Confused by her sister’s sudden change in mood, Jill stayed quiet.'
    >>> rec = TokenisationRecast(package='nltk', method='word')
    >>> rec.setup(text)
    >>> rec.recast()
    ['Grabbing', 'her', 'umbrella', ',', 'Kate', 'raced', 'out', 'of', 'the', 'house', '.', 'Confused', 'by', 'her', 'sister', '’', 's', 'sudden', 'change', 'in', 'mood', ',', 'Jill', 'stayed', 'quiet', '.']
    >>> # OR
    >>> rec.setup_recast(text)
    ['Grabbing', 'her', 'umbrella', ',', 'Kate', 'raced', 'out', 'of', 'the', 'house', '.', 'Confused', 'by', 'her', 'sister', '’', 's', 'sudden', 'change', 'in', 'mood', ',', 'Jill', 'stayed', 'quiet', '.']
    >>> 
    >>> # method='sentence'
    >>> from swachhdata.text import TokenisationRecast
    >>> text = 'You can have a look at our catalogue at www.samplewebsite.com in the services tab'
    >>> rec = TokenisationRecast(package='nltk', method='sentence')
    >>> rec.setup(text)
    >>> rec.recast()
    ['Grabbing her umbrella, Kate raced out of the house.', 'Confused by her sister’s sudden change in mood, Jill stayed quiet.']
    >>> # OR
    >>> rec.setup_recast(text)
    ['Grabbing her umbrella, Kate raced out of the house.', 'Confused by her sister’s sudden change in mood, Jill stayed quiet.']
    """


    def __init__(self, package='nltk', method=None, verbose=0):
        
        if package in ['nltk', 'spacy']:
            super().__init__(verbose=verbose)
            self._package = package
            self._method = method

            if package == 'spacy':
                self._sp = spacy.load('en_core_web_sm')
        else:
            raise ValueError(
                f'Expected package either nltk or spacy, {type(package)} is not a supported package.'
            )
        self._name = 'TokenisationRecast'

    def __nltk_tokenize(self, text):

        if self._method == 'word':
            from nltk.tokenize import word_tokenize
            return word_tokenize(text)
        
        if self._method == 'sentence':
            from nltk.tokenize import sent_tokenize
            return sent_tokenize(text)

    def __spacy_tokenize(self, text):

        text = self._sp(text)

        if self._method == 'word':
            return [word.text for word in text]
        
        if self._method == 'sentence':
            return [sentence for sentence in text.sents]

    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : list of strings
            Processed tokens
        """

        if self._package == 'nltk':
            return self.__nltk_tokenize(text)

        elif self._package == 'spacy':
            return self.__spacy_tokenize(text)

    def recast(self):
        """Perform selected process on the setup text
        
        Returns
        -------
        ntext : list of strings
            Processed tokens
        """
        super().recast()

        data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
        data_tqdm.set_postfix({f'TokenisationRecast [package={self._package}, method={self._method}] process': 'remove'})
        recast_text = [self.__base_recast(text) for text in data_tqdm]
        self.data = recast_text
        return recast_text

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : list of strings
            Processed tokens
        """
        self.setup(text)
        return self.recast()



class StemmingRecast(BaseTextRecast):
    """Recast text data by performing stemming on it.
    
    Parameters
    ----------
    package: string ('nltk', 'extract', 'extract_remove'), default='nltk'
    method: string ('porter', 'snowball')
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> # method='porter'
    >>> from swachhdata.text import StemmingRecast
    >>> text = 'You can have a look at our catalogue at www.samplewebsite.com in the services tab'
    >>> rec = StemmingRecast(method='porter')
    >>> rec.setup(text)
    >>> rec.recast()
    'you can have a look at our catalogu at www.samplewebsite.com in the servic tab'
    >>> # OR
    >>> rec.setup_recast(text)
    'you can have a look at our catalogu at www.samplewebsite.com in the servic tab'
    >>> 
    >>> # method='snowball'
    >>> from swachhdata.text import StemmingRecast
    >>> text = 'You can have a look at our catalogue at www.samplewebsite.com in the services tab'
    >>> rec = StemmingRecast(method='snowball')
    >>> rec.setup(text)
    >>> rec.recast()
    'you can have a look at our catalogu at www.samplewebsite.com in the servic tab'
    >>> # OR
    >>> rec.setup_recast(text)
    'you can have a look at our catalogu at www.samplewebsite.com in the servic tab'
    """


    def __init__(self, package='nltk', method='porter', verbose=0):

        if package in ['nltk', 'spacy']:
            super().__init__(verbose=verbose)
            self._package = package
            self._method = method

        else:
            raise ValueError(
                f'Expected package either nltk or spacy, {type(package)} is not a supported package.'
            )
        self._name = 'StemmingRecast'

    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """

        if self._method == 'porter':
            from nltk.stem.porter import PorterStemmer
            stemmer = PorterStemmer()
        
        elif self._method == 'snowball':
            from nltk.stem.snowball import SnowballStemmer
            stemmer = SnowballStemmer('english')

        words = [stemmer.stem(word) for word in text.split()]
        return ' '.join(words)

    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        super().recast()

        data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
        data_tqdm.set_postfix({f'StemmingRecast [package={self._package}, method={self._method}] process': 'stemming'})
        recast_text = [self.__base_recast(text) for text in data_tqdm]
        self.data = recast_text
        return recast_text

    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        self.setup(text)
        return self.recast()



class LemmatizationRecast(BaseTextRecast):
    """Recast text data by performing lemmatization on it.
    
    Parameters
    ----------
    package: string ('nltk', 'spacy'), default='nltk'
    verbose: int (0, 1, -1), default=0
    

    Examples
    --------
    >>> from swachhdata.text import LemmatizationRecast
    >>> text = 'You can have a look at our catalogue at www.samplewebsite.com in the services tab'
    >>> rec = LemmatizationRecast()
    >>> rec.setup(text)
    >>> rec.recast()
    'You can have a look at our catalogue at www.samplewebsite.com in the service tab'
    >>> # OR
    >>> rec.setup_recast(text)
    'You can have a look at our catalogue at www.samplewebsite.com in the service tab'
    """


    def __init__(self, package='nltk', verbose=0):

        if package in ['nltk', 'spacy']:
            super().__init__(verbose=verbose)
            self._package = package

            if package == 'spacy':
                self._sp = spacy.load('en', disable=['parser', 'ner'])
        else:
            raise ValueError(
                f'Expected package either nltk or spacy, {type(package)} is not a supported package.'
            )
        self._name = 'LemmatizationRecast'

    def __get_wordnet_pos(self, word):
        from nltk.corpus import wordnet

        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {'J': wordnet.ADJ,
                    'N': wordnet.NOUN,
                    'V': wordnet.VERB,
                    'R': wordnet.ADV}

        return tag_dict.get(tag, wordnet.NOUN)

    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """
            
        if self._package == 'nltk':
            import nltk
            from nltk.stem import WordNetLemmatizer
            lemmatizer = WordNetLemmatizer()
            text = ' '.join([lemmatizer.lemmatize(w, self.__get_wordnet_pos(w)) for w in text.split()])
            return text
        
        elif self._package == 'spacy':
            text = self.__sp(text)
            return ' '.join([token.lemma_ for token in text])

    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        super().recast()

        data_tqdm = tqdm(self.data, leave=self._verbose_status, disable=self._verbose)
        data_tqdm.set_postfix({f'LemmatizationRecast [package={self._package}] process': 'lemmatization'})
        recast_text = [self.__base_recast(text) for text in data_tqdm]
        self.data = recast_text
        return recast_text


    def setup_recast(self, text):
        """Change the input text type to supported type
        and
        Perform selected process on the setup text

        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        self.setup(text)
        return self.recast()



def RecastPipeline(text, recastFuncs, **kwargs):
    
    rcount = len(recastFuncs) # recast count
    tcount = len(text) # text length count

    chunk_size = rcount * tcount
    pbar = tqdm(total=chunk_size)

    for rec in recastFuncs:
        text = rec.setup_recast(text)
        pbar.update(tcount)
    
    return text
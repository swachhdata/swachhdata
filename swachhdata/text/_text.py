import re
import pandas
from tqdm.auto import trange, tqdm
from bs4 import BeautifulSoup
from html import unescape
import contractions
import nltk
nltk.download('popular', quiet=True)
import spacy
from gensim.parsing.preprocessing import remove_stopwords
import num2words
import unicodedata
import string
import json
import textblob

from ._base import TextFormatter

class urlRecast(TextFormatter):
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__process = process
        self.__verbose_status = True
        self.__verbose = verbose
        if self.__verbose == -1:
            self.__verbose_status = False
        self.url_ = None
        self.__regex = r'\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b'
        self.get_regex_ = self.__regex

        try:
            assert(isinstance(self.__process, str))
        except:
            print(f'Expected process input type <class \'str\'>, input type received {type(self.__process)}')
        
        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True
    
    
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

        if self.__process == 'remove':
            ntext = ' '.join(re.sub('([@][A-Za-z0-9._:-]+)', ' ', text).split())
            text = re.sub(r'\.{3}', '', text)
            ntext = re.sub(self.__regex, '', text)
            return ntext

        elif self.__process == 'extract':
            text = re.sub(r'\.{3}', '', text)
            url = re.findall(self.__regex, text)
            self.url_ = url
            return url

        elif self.__process == 'extract_remove':
            text = re.sub(r'\.{3}', '', text)
            url = re.findall(self.__regex, text)
            ntext = re.sub(self.__regex, '', text)
            self.url_ = url
            return ntext, url


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
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')
        
        if self._dtype == str:
            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                if self.__process == 'remove' or self.__process == 'extract':
                    ntext = []
                    for text in self._text:
                        ntext.append(self.__base_recast(text))
                    return ntext

                elif self.__process == 'extract_remove':
                    ntext, urls = [], []
                    for text in self._text:
                        text, url = self.__base_recast(text)
                        ntext.append(text)
                        urls.append(url)
                    self.url_ = urls
                    return ntext, urls
                    
            
            if self.__verbose == 1 or self.__verbose == -1:

                if self.__process == 'remove' or self.__process == 'extract':
                    ntext = []
                    progress_bar = trange(self._count, leave=self.__verbose_status)
                    for i in progress_bar:
                        progress_bar.set_postfix({'urlRecast process': self.__process})
                        text = self._text[i]
                        ntext.append(self.__base_recast(text))
                    return ntext

                elif self.__process == 'extract_remove':
                    ntext, urls = [], []
                    progress_bar = trange(self._count, leave=self.__verbose_status)
                    for i in progress_bar:
                        progress_bar.set_postfix({'urlRecast process': self.__process})
                        text = self._text[i]
                        text, url = self.__base_recast(text)
                        ntext.append(text)
                        urls.append(url)
                    self.url_ = urls
                    return ntext, urls


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


##############################################################################################################


class htmlRecast(TextFormatter):
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__verbose_status = True
        self.__verbose = verbose
        if self.__verbose == -1:
            self.__verbose_status = False

        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True
    
    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """

        soup = BeautifulSoup(unescape(text), 'lxml')
        ntext = soup.get_text()
        return ntext


    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings 
            Processed text
        """
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')
        
        if self._dtype == str:

            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                ntext = []
                for text in self._text:
                    ntext.append(self.__base_recast(text))
                return ntext
            
            if self.__verbose == 1 or self.__verbose == -1:

                ntext = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({'htmlRecast process': 'removing'})
                    text = self._text[i]
                    ntext.append(self.__base_recast(text))
                return ntext


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


##############################################################################################################


class EscapeSequenceRecast(TextFormatter):
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__verbose_status = True
        self.__verbose = verbose
        if self.__verbose == -1:
            self.__verbose_status = False

        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True
    
    
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
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')
        
        if self._dtype == str:

            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                ntext = []
                for text in self._text:
                    ntext.append(self.__base_recast(text))
                return ntext
            
            if self.__verbose == 1 or self.__verbose == -1:

                ntext = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({'EscapeSequenceRecast process': 'removing'})
                    text = self._text[i]
                    ntext.append(self.__base_recast(text))
                return ntext


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


##############################################################################################################


class MentionRecast(TextFormatter):
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__process = process
        self.__verbose_status = True
        self.__verbose = verbose
        if self.__verbose == -1:
            self.__verbose_status = False
        self.mention_ = None
        self.__regex = '([@][A-Za-z0-9._:-]+)'
        self.get_regex_ = self.__regex

        try:
            assert(isinstance(self.__process, str))
        except:
            print(f'Expected process input type <class \'str\'>, input type received {type(self.__process)}')
        
        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True
    
    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string (process='remove')
            Processed text
        mention : list of strings (process='extract')
            Extracted Mention(s)
        ntext, mention : string, list of strings (process='extract_remove')
            Processed text, Extracted Mention(s)
        """

        if self.__process == 'remove':
            return ' '.join(re.sub(self.__regex, ' ', text).split())

        elif self.__process == 'extract':
            mention = re.findall(self.__regex, text)
            self.mention_ = mention
            return mention

        elif self.__process == 'extract_remove':
            mention = re.findall(self.__regex, text)
            ntext = ' '.join(re.sub(self.__regex, ' ', text).split())
            self.mention_ = mention
            return ntext, mention


    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings (process='remove')
            Processed text
        mention : list of strings (process='extract')
            Extracted Mention(s)
        ntext, mention : string / list of strings (process='extract_remove')
            Processed text, Extracted Mention(s)
        """
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')
        
        if self._dtype == str:
            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                if self.__process == 'remove' or self.__process == 'extract':
                    ntext = []
                    for text in self._text:
                        ntext.append(self.__base_recast(text))
                    return ntext

                elif self.__process == 'extract_remove':
                    ntext, mentions = [], []
                    for text in self._text:
                        text, mention = self.__base_recast(text)
                        ntext.append(text)
                        mentions.append(mention)
                    self.mention_ = mentions
                    return ntext, mentions
                    
            
            if self.__verbose == 1 or self.__verbose == -1:

                if self.__process == 'remove' or self.__process == 'extract':
                    ntext = []
                    progress_bar = trange(self._count, leave=self.__verbose_status)
                    for i in progress_bar:
                        progress_bar.set_postfix({'MentionRecast process': self.__process})
                        text = self._text[i]
                        ntext.append(self.__base_recast(text))
                    return ntext

                elif self.__process == 'extract_remove':
                    ntext, mentions = [], []
                    progress_bar = trange(self._count, leave=self.__verbose_status)
                    for i in progress_bar:
                        progress_bar.set_postfix({'MentionRecast process': self.__process})
                        text = self._text[i]
                        text, mention = self.__base_recast(text)
                        ntext.append(text)
                        mentions.append(mention)
                    self.mention_ = mentions
                    return ntext, mentions


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
        mention : string / list of strings (process='extract')
            Extracted Mention(s)
        ntext, mention : string / list of strings, list of strings (process='extract_remove')
            Processed text, Extracted Mention(s)
        """

        self.setup(text)
        return self.recast()


##############################################################################################################


class ContractionsRecast(TextFormatter):
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__verbose_status = True
        self.__verbose = verbose
        if self.__verbose == -1:
            self.__verbose_status = False

        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True
    
    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """

        ntext = contractions.fix(text)
        return ntext


    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings 
            Processed text
        """
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')
        
        if self._dtype == str:

            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                ntext = []
                for text in self._text:
                    ntext.append(self.__base_recast(text))
                return ntext
            
            if self.__verbose == 1 or self.__verbose == -1:

                ntext = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({'ContractionsRecast process': 'mapping Contractions'})
                    text = self._text[i]
                    ntext.append(self.__base_recast(text))
                return ntext


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


##############################################################################################################


class CaseRecast(TextFormatter):
    """Recast text data by case formatting the text

    Case formats supported:
        * UPPER case (upper)
        * lower case (lower)
        * First Upper case (fupper)
    
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__process = process
        self.__verbose_status = True
        self.__verbose = verbose
        if self.__verbose == -1:
            self.__verbose_status = False

        try:
            assert(isinstance(self.__process, str))
        except:
            print(f'Expected process input type <class \'str\'>, input type received {type(self.__process)}')
        
        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True
    
    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string (process='remove')
            Processed text
        rec : list of strings (process='extract')
            Extracted rec
        ntext, rec : string, list of strings (process='extract_remove')
            Processed text, Extracted rec
        """

        if self.__process == 'lower':
            return text.lower()

        elif self.__process == 'upper':
            return text.upper()
    
        elif self.__process == 'fupper':
            return text.title()


    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')
        
        if self._dtype == str:
            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                ntext = []
                for text in self._text:
                    ntext.append(self.__base_recast(text))
                return ntext
                    
            if self.__verbose == 1 or self.__verbose == -1:

                ntext = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({'CaseRecast process': self.__process})
                    text = self._text[i]
                    ntext.append(self.__base_recast(text))
                return ntext


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


##############################################################################################################


# class EmojiRecast(TextFormatter):
#     """Recast text data by removing, replaing or extracting Emoji(s).
    
#     Parameters
#     ----------
#     process: string ('remove', 'replace', 'extract', 'extract_remove', 'extract_replace'), default='remove'
#     space_out = bool (True, False), default=False
#     verbose: int (0, 1, -1), default=0

#     Attributes
#     ----------
#     emoji_ : list of emoji(s)
#         extracted emoji(s)
    

#     Examples
#     --------
#     >>> # process='remove'
#     >>> from swachhdata.text import EmojiRecast
#     >>> text = 'Thanks a lot for your wishes! 😊'
#     >>> rec = EmojiRecast(process='remove')
#     >>> rec.setup(text)
#     >>> rec.recast()
#     'Thanks a lot for your wishes!'
#     >>> # OR
#     >>> rec.setup_recast(text)
#     'Thanks a lot for your wishes!'
#     >>> 
#     >>> # process='replace'
#     >>> from swachhdata.text import EmojiRecast
#     >>> text = 'Thanks a lot for your wishes! 😊'
#     >>> rec = EmojiRecast(process='replace')
#     >>> rec.setup(text)
#     >>> rec.recast()
#     'Thanks a lot for your wishes! smiling_face_with_smiling_eyes '
#     >>> # OR
#     >>> rec.setup_recast(text)
#     'Thanks a lot for your wishes! smiling_face_with_smiling_eyes '
#     >>> 
#     >>> # process='extract'
#     >>> from swachhdata.text import EmojiRecast
#     >>> text = 'Thanks a lot for your wishes! 😊'
#     >>> rec = EmojiRecast(process='extract')
#     >>> rec.setup(text)
#     >>> rec.recast()
#     ['😊']
#     >>> # OR
#     >>> rec.setup_recast(text)
#     ['😊']
#     >>> # process='extract_remove'
#     >>> from swachhdata.text import EmojiRecast
#     >>> text = 'Thanks a lot for your wishes! 😊'
#     >>> rec = EmojiRecast(process='extract_remove')
#     >>> rec.setup(text)
#     >>> rec.recast()
#     'Thanks a lot for your wishes!'
#     ['😊']
#     >>> # OR
#     >>> rec.setup_recast(text)
#     'Thanks a lot for your wishes!'
#     ['😊']
#     >>> # process='extract_replace'
#     >>> from swachhdata.text import EmojiRecast
#     >>> text = 'Thanks a lot for your wishes! 😊'
#     >>> rec = EmojiRecast(process='extract_replace')
#     >>> rec.setup(text)
#     >>> rec.recast()
#     'Thanks a lot for your wishes! smiling_face_with_smiling_eyes'
#     ['😊']
#     >>> # OR
#     >>> rec.setup_recast(text)
#     'Thanks a lot for your wishes! smiling_face_with_smiling_eyes'
#     ['😊']
#     """

#     def __init__(self, process='remove', space_out=False, verbose=0):

#         TextFormatter.__init__(self)
#         self.__setup = False
#         self.__process = process
#         self.__space_out = space_out
#         self.__verbose_status = True
#         self.__verbose = verbose
#         if self.__verbose == -1:
#             self.__verbose_status = False
#         self.emoji_ = None
#         self.__emojis_list = list(UNICODE_EMOJI['en'].keys()) + list(UNICODE_EMOJI['es'].keys()) + list(UNICODE_EMOJI['pt'].keys()) + list(UNICODE_EMOJI['it'].keys())

#         try:
#             assert(isinstance(self.__process, str))
#         except:
#             print(f'Expected process input type <class \'str\'>, input type received {type(self.__process)}')
        
#         try:
#             assert(isinstance(self.__verbose, int))
#         except:
#             print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


#     def setup(self, text):
#         """Change the input text type to supported type
#         Parameters
#         ----------
#         text : string / list of strings / pandas.core.series.Series

#         Returns
#         -------
#         self : object
#         """

#         self._dtype = type(text)
#         self._text = text
#         self._TextFormatter__text_formatter()
#         self.__setup = True
    
    
#     def __base_recast(self, text):
#         """Perform selected process on the setup text

#         Parameters
#         ----------
#         text : string / pandas.core.series.Series

#         Returns
#         -------
#         ntext : string (process='remove' / process='replace')
#             Processed text
#         emoji : list of strings (process='extract')
#             Extracted Emojis
#         ntext, emoji : string, list of strings (process='extract_remove' / process='extract_replace')
#             Processed text, Extracted Emojis
#         """
#         if self.__space_out:
#             spaced = ''
#             for char in text:
#                 if char in self.__emojis_list:
#                     spaced += ' '
#                 spaced += char
#             text = spaced
#             text = re.sub(' +', ' ', text)
        
#         if self.__process == 'remove':
#             allchars = [str for str in text]
#             emoji_list = [c for c in allchars if c in self.__emojis_list]
#             text = ' '.join([str for str in text.split() if not any(j in str for j in emoji_list)])
#             return text

#         elif self.__process == 'replace':
#             text = emoji.demojize(text, delimiters=('', ''))
#             return text

#         elif self.__process == 'extract':
#             allchars = [str for str in text]
#             emoji_list = [c for c in allchars if c in self.__emojis_list]
#             self.emoji_ = emoji_list
#             return emoji_list
        
#         elif self.__process == 'extract_remove':
#             allchars = [str for str in text]
#             emoji_list = [c for c in allchars if c in self.__emojis_list]
#             text = ' '.join([str for str in text.split() if not any(j in str for j in emoji_list)])
#             self.emoji_ = emoji_list
#             return text, emoji_list
        
#         elif self.__process == 'extract_replace':
#             allchars = [str for str in text]
#             emoji_list = [c for c in allchars if c in self.__emojis_list]
#             text = emoji.demojize(text, delimiters=('', ''))
#             self.emoji_ = emoji_list
#             return text, emoji_list


#     def recast(self):
#         """
#         Perform selected process on the setup text

#         Returns
#         -------
#         ntext : string / list of strings (process='remove' / process='replace')
#             Processed text
#         emoji : string / list of strings (process='extract')
#             Extracted Emojis
#         ntext, emoji : string / list of strings, list of strings (process='extract_remove' / process='extract_replace')
#             Processed text, Extracted Emojis
#         """
        
#         try:
#             assert(self.__setup)
#         except:
#             print(f'method setup needs to be called before recast')
        
#         if self._dtype == str:
#             return self.__base_recast(self._text)

#         elif self._dtype == list:

#             if self.__verbose == 0:

#                 if self.__process in ['remove', 'replace', 'extract']:
#                     ntext = []
#                     for text in self._text:
#                         ntext.append(self.__base_recast(text))
#                     return ntext

#                 elif self.__process in ['extract_remove', 'extract_replace']:
#                     ntext, emoji_list = [], []
#                     for text in self._text:
#                         text, emoji = self.__base_recast(text)
#                         ntext.append(text)
#                         emoji_list.append(emoji)
#                     self.url_ = emoji_list
#                     return ntext, emoji_list
                    
            
#             if self.__verbose == 1 or self.__verbose == -1:

#                 if self.__process in ['remove', 'replace', 'extract']:
#                     ntext = []
#                     progress_bar = trange(self._count, leave=self.__verbose_status)
#                     for i in progress_bar:
#                         progress_bar.set_postfix({'EmojiRecast process': self.__process})
#                         text = self._text[i]
#                         ntext.append(self.__base_recast(text))
#                     return ntext

#                 elif self.__process in ['extract_remove', 'extract_replace']:
#                     ntext, emoji_list = [], []
#                     progress_bar = trange(self._count, leave=self.__verbose_status)
#                     for i in progress_bar:
#                         progress_bar.set_postfix({'EmojiRecast process': self.__process})
#                         text = self._text[i]
#                         text, emoji = self.__base_recast(text)
#                         ntext.append(text)
#                         emoji_list.append(emoji)
#                     self.url_ = emoji_list
#                     return ntext, emoji_list


#     def setup_recast(self, text):
#         """Change the input text type to supported type
#         and
#         Perform selected process on the setup text

#         Parameters
#         ----------
#         text : string / list of strings / pandas.core.series.Series

#         Returns
#         -------
#         ntext : string / list of strings (process='remove' / process='replace')
#             Processed text
#         emoji : string / list of strings (process='extract')
#             Extracted Emojis
#         ntext, emoji : string / list of strings, list of strings (process='extract_remove' / process='extract_replace')
#             Processed text, Extracted Emojis
#         """

#         self.setup(text)
#         return self.recast()


##############################################################################################################


class HashtagRecast(TextFormatter):
    """Recast text data by removing or extracting Hashtag(s).

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
    """

    def __init__(self, process='remove', verbose=0):

        TextFormatter.__init__(self)
        self.__setup = False
        self.__process = process
        self.__verbose_status = True
        self.__verbose = verbose
        if self.__verbose == -1:
            self.__verbose_status = False
        self.hashtag_ = None
        self.__regex = '([#][A-Za-z0-9_]+)'
        self.get_regex_ = self.__regex

        try:
            assert(isinstance(self.__process, str))
        except:
            print(f'Expected process input type <class \'str\'>, input type received {type(self.__process)}')
        
        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True
    
    
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

        if self.__process == 'remove':
            text = ' '.join(re.sub('([#][A-Za-z0-9_]+)', ' ', text).split())
            return text

        elif self.__process == 'extract':
            hashtag = re.findall('([#][A-Za-z0-9_]+)', text)
            self.hashtag_ = hashtag
            return hashtag

        elif self.__process == 'extract_remove':
            hashtag = re.findall('([#][A-Za-z0-9_]+)', text)
            text = ' '.join(re.sub('([#][A-Za-z0-9_]+)', ' ', text).split())
            self.hashtag_ = hashtag
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
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')
        
        if self._dtype == str:
            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                if self.__process == 'remove' or self.__process == 'extract':
                    ntext = []
                    for text in self._text:
                        ntext.append(self.__base_recast(text))
                    return ntext

                elif self.__process == 'extract_remove':
                    ntext, hashtags = [], []
                    for text in self._text:
                        text, hashtag = self.__base_recast(text)
                        ntext.append(text)
                        hashtags.append(hashtag)
                        self.hashtags_ = hashtags
                    return ntext, hashtags
                    
            
            if self.__verbose == 1 or self.__verbose == -1:

                if self.__process == 'remove' or self.__process == 'extract':
                    ntext = []
                    progress_bar = trange(self._count, leave=self.__verbose_status)
                    for i in progress_bar:
                        progress_bar.set_postfix({'HashtagRecast process': self.__process})
                        text = self._text[i]
                        ntext.append(self.__base_recast(text))
                    return ntext

                elif self.__process == 'extract_remove':
                    ntext, hashtags = [], []
                    progress_bar = trange(self._count, leave=self.__verbose_status)
                    for i in progress_bar:
                        progress_bar.set_postfix({'HashtagRecast process': self.__process})
                        text = self._text[i]
                        text, hashtag = self.__base_recast(text)
                        ntext.append(text)
                        hashtags.append(hashtag)
                        self.hashtags_ = hashtags
                    return ntext, hashtags


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


##############################################################################################################


class ShortWordsRecast(TextFormatter):
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__min_length = min_length
        self.__verbose_status = True
        self.__verbose = verbose
        if self.__verbose == -1:
            self.__verbose_status = False

        try:
            assert(isinstance(self.__min_length, int))
        except:
            print(f'Expected min_length input type <class \'int\'>, input type received {type(self.__min_length)}')

        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True
    
    
    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """

        ntext = []
        for word in text.split():
            if len(word) > self.__min_length:
                ntext.append(word)
        ntext = ' '.join(ntext)
        return ntext


    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings 
            Processed text
        """
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')
        
        if self._dtype == str:

            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                ntext = []
                for text in self._text:
                    ntext.append(self.__base_recast(text))
                return ntext
            
            if self.__verbose == 1 or self.__verbose == -1:

                ntext = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({'ShortWordsRecast [removing] min_length': self.__min_length})
                    text = self._text[i]
                    ntext.append(self.__base_recast(text))
                return ntext


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


##############################################################################################################


class StopWordsRecast(TextFormatter):
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__package = package
        self.__stopWords = None
        self.__verbose_status = True
        self.__verbose = verbose

        if self.__verbose == -1:
            self.__verbose_status = False

        if self.__package == 'custom':
            self.__stopWords = stopwords
            try:
                assert(isinstance(self.__stopWords, list))
            except:
                print(f'Expected stopWords input type <class \'list\'>, input type received {type(self.__stopWords)}')

        try:
            assert(isinstance(self.__package, str))
        except:
            print(f'Expected process input type <class \'str\'>, input type received {type(self.__package)}')
        
        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True
    
    def __setup_package(self):

        if self.__package == 'nltk':
            from nltk.corpus import stopwords
            self.__stopWords = set(stopwords.words('english'))

        elif self.__package == 'spacy':
            sp = spacy.load('en_core_web_sm')
            self.__stopWords = sp.Defaults.stop_words


    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """

        if self.__package == 'nltk':
            ntext = []
            for word in text.split():
                if word not in self.__stopWords:
                    ntext.append(word)
            ntext = ' '.join(ntext)
            return ntext

        elif self.__package == 'spacy':
            ntext = []
            for word in text.split():
                if word not in self.__stopWords:
                    ntext.append(word)
            ntext = ' '.join(ntext)
            return ntext

        elif self.__package == 'gensim':
            text = remove_stopwords(text)
            return text
        
        elif self.__package == 'custom':
            ntext = []
            for word in text.split():
                if word not in self.__stopWords:
                    ntext.append(word)
            ntext = ' '.join(ntext)
            return ntext


    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')
        
        self.__setup_package()

        if self._dtype == str:
            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                ntext = []
                for text in self._text:
                    text = self.__base_recast(text)
                    ntext.append(text)
                return ntext
            
            if self.__verbose == 1 or self.__verbose == -1:

                ntext = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({f'StopWordsRecast [removing] package': self.__package})
                    text = self._text[i]
                    text = self.__base_recast(text)
                    ntext.append(text)
                return ntext


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


##############################################################################################################


class NumberRecast(TextFormatter):
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
    """

    def __init__(self, process='remove', seperator=None, verbose=0):

        TextFormatter.__init__(self)
        self.__setup = False
        self.__process = process
        self.__seperator = seperator
        self.__verbose_status = True
        self.__verbose = verbose
        if self.__verbose == -1:
            self.__verbose_status = False
        self.number_ = None

        try:
            assert(isinstance(self.__process, str))
        except:
            print(f'Expected process input type <class \'str\'>, input type received {type(self.__process)}')
        
        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True
    
    
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
        if self.__seperator == ',':
            text = re.sub(r'(?<!\B)[,](?!\B)', '', text)
        
        if self.__seperator == '.':
            text = re.sub(r'(?<!\B)[.](?!\B)', '', text)
        
        if self.__process == 'remove':
            return re.sub(r'[0-9]+', '', text, 0)

        elif self.__process == 'replace':
            return re.sub(r'(\d+)', lambda x: num2words.num2words(int(x.group(0))), text, 0)

        elif self.__process == 'extract':
            return re.findall(r'[0-9]+', text, 0)
        
        elif self.__process == 'extract_remove':
            self.number_ = re.findall(r'[0-9]+', text, 0)
            text = re.sub(r'[0-9]+', '', text, 0)
            return text, self.number_
        
        elif self.__process == 'extract_replace':
            self.number_ = re.findall(r'[0-9]+', text, 0)
            text = re.sub(r'(\d+)', lambda x: num2words.num2words(int(x.group(0))), text, 0)
            return text, self.number_


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
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')
        
        if self._dtype == str:
            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                if self.__process in ['remove', 'replace', 'extract']:
                    ntext = []
                    for text in self._text:
                        ntext.append(self.__base_recast(text))
                    return ntext

                elif self.__process in ['extract_remove', 'extract_replace']:
                    ntext, number_list = [], []
                    for text in self._text:
                        text, number = self.__base_recast(text)
                        ntext.append(text)
                        number_list.append(number)
                    self.number_ = number_list
                    return ntext, number_list
                    
            
            if self.__verbose == 1 or self.__verbose == -1:

                if self.__process in ['remove', 'replace', 'extract']:
                    ntext = []
                    progress_bar = trange(self._count, leave=self.__verbose_status)
                    for i in progress_bar:
                        progress_bar.set_postfix({'NumberRecast process': self.__process})
                        text = self._text[i]
                        ntext.append(self.__base_recast(text))
                    return ntext

                elif self.__process in ['extract_remove', 'extract_replace']:
                    ntext, number_list = [], []
                    progress_bar = trange(self._count, leave=self.__verbose_status)
                    for i in progress_bar:
                        progress_bar.set_postfix({'NumberRecast process': self.__process})
                        text = self._text[i]
                        text, number = self.__base_recast(text)
                        ntext.append(text)
                        number_list.append(number)
                    self.number_ = number_list
                    return ntext, number_list


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


##############################################################################################################


class AlphabetRecast(TextFormatter):
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__process = process
        self.__verbose_status = True
        self.__verbose = verbose
        if self.__verbose == -1:
            self.__verbose_status = False

        # try:
        #     assert(isinstance(self.__process, str))
        # except:
        #     print(f'Expected process input type <class \'str\'>, input type received {type(self.__process)}')
        
        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True
    
    
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
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')
        
        if isinstance(self.__process, list):

            for process in self.__process:

                if self._dtype == str:
                    self._text = self.__base_recast(self._text, process)

                elif self._dtype == list:

                    if self.__verbose == 0:

                        ntext = []
                        for text in self._text:
                            ntext.append(self.__base_recast(text, process))
                        self._text = ntext

                    if self.__verbose == 1 or self.__verbose == -1:

                        ntext = []
                        progress_bar = trange(self._count, leave=False)
                        for i in progress_bar:
                            progress_bar.set_postfix({'AlphabetRecast process': process})
                            text = self._text[i]
                            ntext.append(self.__base_recast(text, process))
                        self._text = ntext
            
            return self._text
        
        elif isinstance(self.__process, str):

            if self._dtype == str:
                return self.__base_recast(self._text, self.__process)

            elif self._dtype == list:

                if self.__verbose == 0:

                    ntext = []
                    for text in self._text:
                        ntext.append(self.__base_recast(text, self.__process))
                    return ntext

                if self.__verbose == 1 or self.__verbose == -1:

                    ntext = []
                    progress_bar = trange(self._count, leave=self.__verbose_status)
                    for i in progress_bar:
                        progress_bar.set_postfix({'AlphabetRecast process': self.__process})
                        text = self._text[i]
                        ntext.append(self.__base_recast(text, self.__process))
                    return ntext


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


##############################################################################################################


class PunctuationRecast(TextFormatter):
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__verbose_status = True
        self.__verbose = verbose
        if self.__verbose == -1:
            self.__verbose_status = False
        
        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True
    
    
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
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')


        if self._dtype == str:
            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                ntext = []
                for text in self._text:
                    ntext.append(self.__base_recast(text))
                return ntext

            if self.__verbose == 1 or self.__verbose == -1:

                ntext = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({'PunctuationRecast process': 'removing'})
                    text = self._text[i]
                    ntext.append(self.__base_recast(text))
                return ntext


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


##############################################################################################################


class TokenisationRecast(TextFormatter):
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__package = package
        self.__method = method
        self.__verbose_status = True
        self.__verbose = verbose

        if self.__verbose == -1:
            self.__verbose_status = False

        elif self.__package == 'spacy':
            self.__sp = spacy.load('en_core_web_sm')

        try:
            assert(isinstance(self.__package, str))
        except:
            print(f'Expected process input type <class \'str\'>, input type received {type(self.__package)}')
        
        try:
            assert(isinstance(self.__method, str))
        except:
            print(f'Expected method input type <class \'str\'>, input type received {type(self.__method)}')
        
        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True


    def __nltk_tokenize(self, text):

        if self.__method == 'word':
            from nltk.tokenize import word_tokenize
            return word_tokenize(text)
        
        if self.__method == 'sentence':
            from nltk.tokenize import sent_tokenize
            return sent_tokenize(text)


    def __spacy_tokenize(self, text):

        text = self.__sp(text)

        if self.__method == 'word':
            return [word.text for word in text]
        
        if self.__method == 'sentence':
            return [sentence for sentence in text.sents]


    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : list of strings
            Processed tokens
        """

        if self.__package == 'nltk':
            return self.__nltk_tokenize(text)

        elif self.__package == 'spacy':
            return self.__spacy_tokenize(text)


    def recast(self):
        """Perform selected process on the setup text
        
        Returns
        -------
        ntext : list of strings
            Processed tokens
        """
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')

        if self._dtype == str:
            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                ntext = []
                for text in self._text:
                    text = self.__base_recast(text)
                    ntext.append(text)
                return ntext
            
            if self.__verbose == 1 or self.__verbose == -1:

                ntext = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({f'TokenisationRecast {self.__package} process': f'{self.__method} tokenisation'})
                    text = self._text[i]
                    text = self.__base_recast(text)
                    ntext.append(text)
                return ntext


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


##############################################################################################################


class StemmingRecast(TextFormatter):
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__package = package
        self.__method = method
        self.__verbose_status = True
        self.__verbose = verbose

        if self.__verbose == -1:
            self.__verbose_status = False

        try:
            assert(isinstance(self.__package, str))
        except:
            print(f'Expected process input type <class \'str\'>, input type received {type(self.__package)}')
        
        try:
            assert(isinstance(self.__method, str))
        except:
            print(f'Expected method input type <class \'str\'>, input type received {type(self.__method)}')
        
        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True


    def __base_recast(self, text):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string
            Processed text
        """

        if (self.__verbose == 1 or self.__verbose == -1) and self._dtype == str:

            if self.__method == 'porter':
                from nltk.stem.porter import PorterStemmer
                porter_stemmer = PorterStemmer()
                words = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({f'StemmingRecast process': f'{self.__method} stemmer'})
                    word = text.split()[i]
                    words.append(porter_stemmer.stem(word))
                return ' '.join(words)

            elif self.__method == 'snowball':
                from nltk.stem.snowball import SnowballStemmer
                snowball_stemmer = SnowballStemmer('english')
                words = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({f'StemmingRecast process': f'{self.__method} stemmer'})
                    word = text.split()[i]
                    words.append(snowball_stemmer.stem(word))
                return ' '.join(words)
        
        else:

            if self.__method == 'porter':
                from nltk.stem.porter import PorterStemmer
                porter_stemmer = PorterStemmer()
                words = []
                for word in text.split():
                    words.append(porter_stemmer.stem(word))
                return ' '.join(words)

            elif self.__method == 'snowball':
                from nltk.stem.snowball import SnowballStemmer
                snowball_stemmer = SnowballStemmer('english')
                words = []
                for word in text.split():
                    words.append(snowball_stemmer.stem(word))
                return ' '.join(words)


    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """
        
        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')

        if self._dtype == str:
            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                ntext = []
                for text in self._text:
                    text = self.__base_recast(text)
                    ntext.append(text)
                return ntext
            
            if self.__verbose == 1 or self.__verbose == -1:

                ntext = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({f'StemmingRecast process': f'{self.__method} stemmer'})
                    text = self._text[i]
                    text = self.__base_recast(text)
                    ntext.append(text)
                return ntext


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


##############################################################################################################


class LemmatizationRecast(TextFormatter):
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

        TextFormatter.__init__(self)
        self.__setup = False
        self.__package = package
        self.__verbose_status = True
        self.__verbose = verbose

        if self.__verbose == -1:
            self.__verbose_status = False
        
        elif self.__package == 'spacy':
            self.__sp = spacy.load('en', disable=['parser', 'ner'])

        try:
            assert(isinstance(self.__package, str))
        except:
            print(f'Expected process input type <class \'str\'>, input type received {type(self.__package)}')
        
        try:
            assert(isinstance(self.__verbose, int))
        except:
            print(f'Expected verbose input type <class \'int\'>, input type received {type(self.__verbose)}')


    def setup(self, text):
        """Change the input text type to supported type
        Parameters
        ----------
        text : string / list of strings / pandas.core.series.Series

        Returns
        -------
        self : object
        """

        self._dtype = type(text)
        self._text = text
        self._TextFormatter__text_formatter()
        self.__setup = True


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

        if (self.__verbose == 1 or self.__verbose == -1) and self._dtype == str:

            if self.__package == 'nltk':
                import nltk
                from nltk.stem import WordNetLemmatizer
                lemmatizer = WordNetLemmatizer()
                words = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({f'LemmatizationRecast process': f'{self.__package} lemmatizer'})
                    w = text.split()[i]
                    words.append(lemmatizer.lemmatize(w, self.__get_wordnet_pos(w)))
                return ' '.join(words)
            
            elif self.__package == 'spacy':
                text = self.__sp(text)
                return ' '.join([token.lemma_ for token in text])
        
        else:
            
            if self.__package == 'nltk':
                import nltk
                from nltk.stem import WordNetLemmatizer
                lemmatizer = WordNetLemmatizer()
                text = ' '.join([lemmatizer.lemmatize(w, self.__get_wordnet_pos(w)) for w in text.split()])
                return text
            
            elif self.__package == 'spacy':
                text = self.__sp(text)
                return ' '.join([token.lemma_ for token in text])


    def recast(self):
        """Perform selected process on the setup text

        Returns
        -------
        ntext : string / list of strings
            Processed text
        """

        try:
            assert(self.__setup)
        except:
            print(f'method setup needs to be called before recast')

        if self._dtype == str:
            return self.__base_recast(self._text)

        elif self._dtype == list:

            if self.__verbose == 0:

                ntext = []
                for text in self._text:
                    text = self.__base_recast(text)
                    ntext.append(text)
                return ntext
            
            if self.__verbose == 1 or self.__verbose == -1:

                ntext = []
                progress_bar = trange(self._count, leave=self.__verbose_status)
                for i in progress_bar:
                    progress_bar.set_postfix({f'LemmatizationRecast process': f'{self.__package} lemmatizer'})
                    text = self._text[i]
                    text = self.__base_recast(text)
                    ntext.append(text)
                return ntext


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


##############################################################################################################


def TextRecast(text, **kwargs):
    """TextRecast: wrapper function for Recast classes.
    
    Parameters
    ----------
    text : string / list of strings / pandas.core.series.Series
    **kwargs

    kwargs Template
    ----------
    { urlRecast = {'process': 'extract_remove'},
      htmlRecast = True,
      EscapeSequenceRecast = True,
      MentionRecast = {'process': 'extract_remove'},
      ContractionsRecast = True,
      CaseRecast = {'process': 'lower'},
      EmojiRecast = {'process': 'extract_remove', 'space_out': False},
      HashtagRecast = {'process': 'extract_remove'},
      ShortWordsRecast = {'min_length': 3},
      StopWordsRecast = {'package': 'nltk', 'space_out': None},
      NumberRecast = {'process': 'remove', 'seperator': None},
      AlphabetRecast = {'process': 'all'},
      PunctuationRecast = True,
      StemmingRecast = {'package': 'nltk', 'method': 'porter'},
      LemmatizationRecast = {'package':'nltk'},
      TokenisationRecast = {'package': 'nltk', 'method': 'sentence' }

    Attributes
    ----------
    * url
    * mention
    * emoji
    * hashtag
    * token
    * number

    Returns
    ---------
    ntext : string / list of strings
            Processed text
    """

    verbose=-1

    ccount = 0 # complete count
    rcount = len(kwargs) # recast count
    tcount = len(text) # text length count

    chunk_size = rcount * tcount
    pbar = tqdm(total=chunk_size)

    if 'urlRecast' in kwargs:
        
        ccount +=  1
        pbar.set_postfix({'urlRecast || TextRecast No': f'{ccount}/{rcount}'})

        global url
        if kwargs['urlRecast']['process'] == 'extract_remove':
           text, url  = urlRecast(kwargs['urlRecast']['process'], verbose=verbose).setup_recast(text)

        elif kwargs['urlRecast']['process'] == 'extract':
            url  = urlRecast(kwargs['urlRecast']['process'], verbose=verbose).setup_recast(text)
        
        elif kwargs['urlRecast']['process'] == 'remove':
           text = urlRecast(kwargs['urlRecast']['process'], verbose=verbose).setup_recast(text) 

        pbar.update(tcount)

    if 'htmlRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'htmlRecast || TextRecast No': f'{ccount}/{rcount}'})

        text = htmlRecast(verbose=verbose).setup_recast(text)
        pbar.update(tcount)
    
    if 'EscapeSequenceRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'EscapeSequenceRecast || TextRecast No': f'{ccount}/{rcount}'})

        text = EscapeSequenceRecast(verbose=verbose).setup_recast(text)
        pbar.update(tcount)
    
    if 'MentionRecast' in kwargs:
        
        ccount +=  1
        pbar.set_postfix({'MentionRecast || TextRecast No': f'{ccount}/{rcount}'})

        global mention
        if kwargs['MentionRecast']['process'] == 'extract_remove':
           text, mention  = MentionRecast(kwargs['MentionRecast']['process'], verbose=verbose).setup_recast(text)

        elif kwargs['MentionRecast']['process'] == 'extract':
            mention  = MentionRecast(kwargs['MentionRecast']['process'], verbose=verbose).setup_recast(text)
        
        elif kwargs['MentionRecast']['process'] == 'remove':
           text = MentionRecast(kwargs['MentionRecast']['process'], verbose=verbose).setup_recast(text)

        pbar.update(tcount)

    if 'ContractionsRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'ContractionsRecast || TextRecast No': f'{ccount}/{rcount}'})

        text = ContractionsRecast(verbose=verbose).setup_recast(text)
        pbar.update(tcount)
    
    if 'CaseRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'CaseRecast || TextRecast No': f'{ccount}/{rcount}'})

        text = CaseRecast(kwargs['CaseRecast']['process'], verbose=verbose).setup_recast(text)
        pbar.update(tcount)
    
    # if 'EmojiRecast' in kwargs:

    #     ccount +=  1
    #     pbar.set_postfix({'EmojiRecast || TextRecast No': f'{ccount}/{rcount}'})
        
    #     global emoji
    #     if kwargs['EmojiRecast']['process'] == 'extract_remove':
    #        text, emoji  = EmojiRecast(kwargs['EmojiRecast']['process'], kwargs['EmojiRecast']['space_out'], verbose=verbose).setup_recast(text)

    #     elif kwargs['EmojiRecast']['process'] == 'extract':
    #         emoji  = EmojiRecast(kwargs['EmojiRecast']['process'], kwargs['EmojiRecast']['space_out'], verbose=verbose).setup_recast(text)
        
    #     elif kwargs['EmojiRecast']['process'] == 'remove':
    #        text = EmojiRecast(kwargs['EmojiRecast']['process'], kwargs['EmojiRecast']['space_out'], verbose=verbose).setup_recast(text)

    #     pbar.update(tcount)
    
    if 'HashtagRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'HashtagRecast || TextRecast No': f'{ccount}/{rcount}'})

        global hashtag
        if kwargs['HashtagRecast']['process'] == 'extract_remove':
           text, hashtag  = HashtagRecast(kwargs['HashtagRecast']['process'], verbose=verbose).setup_recast(text)

        elif kwargs['HashtagRecast']['process'] == 'extract':
            hashtag  = HashtagRecast(kwargs['HashtagRecast']['process'], verbose=verbose).setup_recast(text)
        
        elif kwargs['HashtagRecast']['process'] == 'remove':
           text = HashtagRecast(kwargs['HashtagRecast']['process'], verbose=verbose).setup_recast(text)
        
        pbar.update(tcount)
    
    if 'ShortWordsRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'ShortWordsRecast || TextRecast No': f'{ccount}/{rcount}'})

        text = ShortWordsRecast(kwargs['ShortWordsRecast']['min_length'], verbose=verbose).setup_recast(text)
        pbar.update(tcount)

    if 'StopWordsRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'StopWordsRecast || TextRecast No': f'{ccount}/{rcount}'})

        text = StopWordsRecast(kwargs['StopWordsRecast']['package'], kwargs['StopWordsRecast']['stopwords'], verbose=verbose).setup_recast(text)
        pbar.update(tcount)

    if 'NumberRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'NumberRecast || TextRecast No': f'{ccount}/{rcount}'})

        global number
        if kwargs['NumberRecast']['process'] == 'extract_remove' or kwargs['NumberRecast']['process'] == 'extract_replace':
           text, number  = NumberRecast(kwargs['NumberRecast']['process'], kwargs['NumberRecast']['seperator'], verbose=verbose).setup_recast(text)

        elif kwargs['NumberRecast']['process'] == 'extract':
            number  = NumberRecast(kwargs['NumberRecast']['process'], kwargs['NumberRecast']['seperator'], verbose=verbose).setup_recast(text)
        
        elif kwargs['NumberRecast']['process'] == 'remove' or kwargs['NumberRecast']['process'] == 'replace':
           text = NumberRecast(kwargs['NumberRecast']['process'], kwargs['NumberRecast']['seperator'], verbose=verbose).setup_recast(text)
        
        pbar.update(tcount)

    if 'AlphabetRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'AlphabetRecast || TextRecast No': f'{ccount}/{rcount}'})

        text = AlphabetRecast(kwargs['AlphabetRecast']['process'], verbose=verbose).setup_recast(text)
        pbar.update(tcount)

    if 'PunctuationRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'PunctuationRecast || TextRecast No': f'{ccount}/{rcount}'})

        text = PunctuationRecast(verbose=verbose).setup_recast(text)
        pbar.update(tcount)

    if 'StemmingRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'StemmingRecast || TextRecast No': f'{ccount}/{rcount}'})

        text = StemmingRecast(kwargs['StemmingRecast']['package'], kwargs['StemmingRecast']['method'], verbose=verbose).setup_recast(text)
        pbar.update(tcount)

    if 'LemmatizationRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'LemmatizationRecast || TextRecast No': f'{ccount}/{rcount}'})

        text = LemmatizationRecast(kwargs['LemmatizationRecast']['package'], verbose=verbose).setup_recast(text)
        pbar.update(tcount)

    if 'TokenisationRecast' in kwargs:

        ccount +=  1
        pbar.set_postfix({'TokenisationRecast || TextRecast No': f'{ccount}/{rcount}'})

        global token
        token = TokenisationRecast(kwargs['TokenisationRecast']['package'], kwargs['TokenisationRecast']['method'], verbose=verbose).setup_recast(text)
        pbar.update(tcount)

    pbar.set_postfix({'TextRecast Complete! || TextRecast No': f'{ccount}/{rcount}'})
    pbar.close()
    
    return text


##############################################################################################################


      
def RecastPipeline(text, recastFuncs, **kwargs):

    ccount = 0 # complete count
    rcount = len(recastFuncs) # recast count
    tcount = len(text) # text length count

    chunk_size = rcount * tcount
    pbar = tqdm(total=chunk_size)

    for rec in recastFuncs:
        text = rec.setup_recast(text)
        pbar.update(tcount)
    
    return text

import re
import nltk

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

from bs4 import BeautifulSoup
from html import unescape
import contractions
import unicodedata
import num2words
import pandas
import string
from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords
from textblob import TextBlob, Word
from operator import add
from itertools import starmap
from nltk.stem import LancasterStemmer

lancaster = LancasterStemmer()
stopWords = set(stopwords.words('english'))
word = WhitespaceTokenizer()

class TextSetup:
    def __init__(self, text):
        self.t = text
        self.text = self.t
        self.dtype_str = isinstance(self.text, str)
        self.dtype_list = isinstance(self.text, list)
        self.dtype_pd_series = isinstance(self.text, pandas.core.series.Series)
        if self.dtype_pd_series:
            self.t = text.tolist()
            self.text = self.t

class SwachhText(TextSetup):

    def __init__(self, TextSetup):
        self.t = TextSetup.t
        self.text = self.t
        self.dtype_str = isinstance(self.text, str)
        self.dtype_list = isinstance(self.text, list)
        self.dtype_pd_series = isinstance(self.text, pandas.core.series.Series)

    
    def remove_url(self):
        
        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(re.sub(r'http\S+', '', i))
            return ntext
            
        elif self.dtype_str:
            ntext = re.sub(r'http\S+', '', self.text)
            return ntext
        

    def remove_html(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                soup = BeautifulSoup(unescape(i), 'lxml')
                ntext.append(soup.get_text())
            return ntext
            
        elif self.dtype_str:
            soup = BeautifulSoup(unescape(self.text), 'lxml')
            ntext = soup.get_text()
            return ntext

    def remove_line_break(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(i.replace('\r', ' ').replace('\n', ' '))
            return ntext
            
        elif self.dtype_str:
            ntext = self.text.replace('\r', ' ').replace('\n', ' ')
            return ntext
        
    def remove_mention(self):
        
        if self.dtype_list:
            ntext = []
            for i in self.text:
                no_mention = ' '.join(re.sub('([@][A-Za-z0-9._:-]+)', ' ', i).split())
                ntext.append(no_mention)
            return ntext
            
        elif self.dtype_str:
            no_mention = ' '.join(re.sub('([@][A-Za-z0-9._:-]+)', ' ', self.text).split())
            ntext = no_mention
            return ntext
    
    def map_contraction(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(contractions.fix(i))
            return ntext    
            
        elif self.dtype_str:
            ntext = contractions.fix(self.text)
            return ntext

    def lower_case(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(i.lower())
            return ntext
            
        elif self.dtype_str:
            ntext = self.text.lower()
            return ntext
        
    def remove_accented_char(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(unicodedata.normalize('NFKD', i).encode('ascii', 'ignore').decode('utf-8', 'ignore'))
            return ntext
            
        elif self.dtype_str:
            ntext = unicodedata.normalize('NFKD', self.text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            return ntext
        
    def remove_non_ascii(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(re.sub(r'[^\x00-\x7F]+', ' ', i))
            return ntext
            
        elif self.dtype_str:
            ntext = re.sub(r'[^\x00-\x7F]+', ' ', self.text)
            return ntext
        
    def remove_num_no_comma(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(re.sub(r'(?<!\B)[,](?!\B)', '', i, 0))
            return ntext
            
        elif self.dtype_str:
            ntext = re.sub(r'(?<!\B)[,](?!\B)', '', self.text, 0)
            return ntext
        
    def replace_number(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(re.sub(r'(\d+)', lambda x: num2words.num2words(int(x.group(0))), i))
            return ntext
            
        elif self.dtype_str:
            ntext = re.sub(r'(\d+)', lambda x: num2words.num2words(int(x.group(0))), self.text)
            return ntext
        
    def remove_num_punctuation(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(re.sub(r'(?<!\B)[,.](?!\B)', '', i, 0))
            return ntext
            
        elif self.dtype_str:
            ntext = re.sub(r'(?<!\B)[,.](?!\B)', '', self.text, 0)
            return ntext
        
    def remove_number(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(re.sub(r'[0-9]+', '', i, 0))
            return ntext
            
        elif self.dtype_str:
            ntext = re.sub(r'[0-9]+', '', self.text, 0)
            return ntext
        
    def extract_hashtag(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(re.findall('#\w+', i))
            return ntext
            
        elif self.dtype_str:
            ntext = re.findall('#\w+', self.text)
            return ntext
        
    def remove_hashtag(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                no_hashtag = ' '.join(re.sub('([#][A-Za-z0-9._:-]+)',' ',i).split())
                ntext.append(no_hashtag)
            return ntext
            
        elif self.dtype_str:
            ntext = ' '.join(re.sub('([#][A-Za-z0-9._:-]+)', ' ', self.text).split())
            return ntext
        
    def remove_punctuation(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(i.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).replace(' '*4, ' ').replace(' '*3, ' ').replace(' '*2, ' ').strip())
            return ntext
            
        elif self.dtype_str:
            ntext = self.text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).replace(' '*4, ' ').replace(' '*3, ' ').replace(' '*2, ' ').strip()
            return ntext
        
    def keep_alphabet(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(re.sub(r'[^a-zA-Z]', ' ', i, 0))
            return ntext
            
        elif self.dtype_str:
            ntext = re.sub(r'[^a-zA-Z]', ' ', self.text, 0)
            return ntext
        
    def tokenize_text(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(word.tokenize(i))
            return ntext
            
        elif self.dtype_str:
            ntext = word.tokenize(self.text)
            return ntext
            
    def remove_stopword(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                nword = []
                for word in i:
                    if word not in stopWords:
                        nword.append(word)
                ntext.append(nword)
            return ntext
            
        elif self.dtype_str:
            ntext = []
            for word in self.text:
                if word not in stopWords:
                    ntext.append(word)
            return ntext
        
    def remove_shortword(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                nword=[]
                for word in i:
                    if len(word) > 3:
                        nword.append(word)
                ntext.append(nword)
            return ntext
            
        elif self.dtype_str:
            ntext = []
            for word in self.text:
                if len(word) > 3:
                    ntext.append(word)
            return ntext
        
    def join_words(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                ntext.append(' '.join(i))
            return ntext
            
        elif self.dtype_str:
            ntext = ' '.join(self.text)
            return ntext
        
    def stemming(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                nword=[]
                for word in i:
                    nword.append(lancaster.stem(word))
                ntext.append(''.join(nword))
            return ntext
    
        elif self.dtype_str:
            ntext = []
            for word in self.text:
                ntext.append(lancaster.stem(word))
            return ''.join(ntext)
        
    def lemmatize_with_postag(self):

        if self.dtype_list:
            ntext = []
            for i in self.text:
                sent = TextBlob(i)
                tag_dict = {'J': 'a', 
                            'N': 'n', 
                            'V': 'v', 
                            'R': 'r'}
                words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in sent.tags]    
                lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
                ntext.append(' '.join(lemmatized_list))
            return ntext
            
        elif self.dtype_str:
            sent = TextBlob(self.text)
            tag_dict = {'J': 'a', 
                        'N': 'n', 
                        'V': 'v', 
                        'R': 'r'}
            words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in sent.tags]    
            lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
            ntext = ' '.join(lemmatized_list)
            return ntext

class SwachhSabText(SwachhText):

    def __init__(self, SwachhText):
        self.t = SwachhText.t
        self.text = self.t
        self.dtype_str = isinstance(self.text, str)
        self.dtype_list = isinstance(self.text, list)
        self.dtype_pd_series = isinstance(self.text, pandas.core.series.Series)

    
    def clean_text(self, verbose=False, **kwargs):
        
        if verbose:
            print('Initializing...\n')
        self.text = self.t
        
        if 'rem_url' in kwargs and kwargs['rem_url']:
            if verbose:
                print('Removing URLs...')
            self.text = SwachhText.remove_url(self)

        if 'rem_html' in kwargs and kwargs['rem_html']:
            if verbose:
                print('Removing HTML tags...')
            self.text = SwachhText.remove_html(self)

        if 'rem_linebreak' in kwargs and kwargs['rem_linebreak']:
            if verbose:
                print('Removing breaks...')
            self.text = SwachhText.remove_line_break(self)

        if 'rem_mention' in kwargs and kwargs['rem_mention']:
            if verbose:
                print('Removing mentions...')
            self.text = SwachhText.remove_mention(self)

        if 'exp_contraction' in kwargs and kwargs['exp_contraction']:
            if verbose:
                print('Expanding contractions...')
            self.text = SwachhText.map_contraction(self)
        
        if 'lower_case' in kwargs and kwargs['lower_case']:
            self.text = SwachhText.lower_case(self)

        if 'rem_acc_char' in kwargs and kwargs['rem_acc_char']:
            if verbose:
                print('Removing accented characters...')
            self.text = SwachhText.remove_accented_char(self)

        if 'rem_non_ascii_char' in kwargs and kwargs['rem_non_ascii_char']:
            if verbose:
                print('Removing non ASCII characters...')
            self.text = SwachhText.remove_non_ascii(self)

        if 'rep_num' in kwargs and kwargs['rep_num']:
            if verbose:
                print('Replacing numbers...')
            self.text = SwachhText.remove_num_no_comma(self)
            self.text = SwachhText.replace_number(self)

        if 'rem_num' in kwargs and kwargs['rem_num']:
            if verbose:
                print('Removing numbers...')
            self.text = SwachhText.remove_num_punctuation(self)
            self.text = SwachhText.remove_number(self)

        if 'get_hashtag' in kwargs and kwargs['get_hashtag']:
            if verbose:
                print('Extracting hashtags...')
            self.hashtags = SwachhText.extract_hashtag(self)

        if 'rem_hashtag' in kwargs and kwargs['rem_hashtag']:
            if verbose:
                print('Removing hashtags...')
            self.text = SwachhText.remove_hashtag(self)

        if 'rem_punct' in kwargs and kwargs['rem_punct']:
            if verbose:
                print('Removing punctuations...')
            self.text = SwachhText.remove_punctuation(self)

        if 'keep_alpha' in kwargs and kwargs['keep_alpha']:
            if verbose:
                print('Filtering out non alphabets...')
            self.text = SwachhText.keep_alphabet(self)

        if 'tokenisation' in kwargs and kwargs['tokenisation']:
            if verbose:
                print('Tokenising...')
            self.text = SwachhText.tokenize_text(self)

        if 'rem_stop_word' in kwargs and kwargs['rem_stop_word']:
            if verbose:
                print('Removing stop words...')
            if 'tokenisation' in kwargs and kwargs['tokenisation']:
                self.text = SwachhText.remove_stopword(self)
            else:
                self.text = SwachhText.tokenize_text(self)
                self.text = SwachhText.remove_stopword(self)
                self.text = SwachhText.join_words(self)

        if 'rem_short_word' in kwargs and kwargs['rem_short_word']:
            if verbose:
                print('Removing short words...')
            if 'tokenisation' in kwargs and kwargs['tokenisation']:
                self.text = SwachhText.remove_shortword(self)
                self.text = SwachhText.join_words(self)
            else:
                self.text = SwachhText.tokenize_text(self)
                self.text = SwachhText.remove_shortword(self)
                self.text = SwachhText.join_words(self)

        if 'join_word' in kwargs and kwargs['join_word']:
            self.text = SwachhText.join_words(self)

        if 'stemming' in kwargs and kwargs['stemming']:
            if verbose:
                print('Stemming...')
            self.text = SwachhText.stemming(self)

        if 'lemmatization' in kwargs and kwargs['lemmatization']:
            if verbose:
                print('Lemmatizing...')
            self.text = SwachhText.lemmatize_with_postag(self)
        
        if verbose:
            print('\nComplete!\n')
        
        return self.text
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


class TextFormatter:
    """
    Base Data Formatter for all recasts in swachhdata.text module

    Accepted text input format:
        * string
        * list of string
        * pandas.core.series.Series
    """

    def __init__(self):
        
        self._dtype = None
        self._text = None
        self._count = None

    
    def __text_formatter(self):
        
        self._count = len(self._text)

        if self._dtype == pandas.core.series.Series:
            self._text = self._text.tolist()
            self._dtype = type(self._text)

        if self._dtype == str:
            self._count = len(self._text.split())
            self._dtype = type(self._text)
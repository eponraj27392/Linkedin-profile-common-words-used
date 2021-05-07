# -*- coding: utf-8 -*-
"""
Created on Wed May  5 00:27:12 2021

@author: eponr
"""

import re
import string
import numpy as np
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

import nltk
# nltk.download('stopwords')





class PreprocessText:
    def process_text(self, post_text):
        """Process the text.
        Input:
            post_text: a string containing a post text
        Output:
            post_text_clean: a list of words containing the processed post_text
        """
        stemmer = PorterStemmer()
        stopwords_english = stopwords.words('english')
        # remove tickers like $GE
        post_text = re.sub(r'\$\w*', '', post_text)
        # remove hyperlinks
        post_text = re.sub(r'https?:\/\/.*[\r\n]*', '', post_text)
        # remove hashtags
        # only removing the hash # sign from the word
        post_text = re.sub(r'#', '', post_text)
        # tokenize the text
        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                                   reduce_len=True)
        post_text_tokens = tokenizer.tokenize(post_text)
    
        post_text_clean = []
        for word in post_text_tokens:
            if (word not in stopwords_english) and (word not in string.punctuation + '’' + '…' + '___' + '–'):  # remove punctuation
                #word = stemmer.stem(word)  # stemming word
                post_text_clean.append(word)
    
        return post_text_clean
    
    
    def build_freqs(self, df):
        """Build frequencies.
        Input:
            post_text_clean: a list of post_text_clean
        Output:
            freqs: a dictionary mapping each word pair to its frequency
        """
    
    
        # Start with an empty dictionary and populate it by looping over all post_text_clean
        # and over all processed words in each post_text_clean.
        freqs = {}
        for idx in range(len(df)):
            for clean_word in self.process_text(df.loc[idx, 'Post Text']):
                if clean_word in freqs:
                    freqs[clean_word] += 1
                else:
                    freqs[clean_word] = 1
    
        return freqs
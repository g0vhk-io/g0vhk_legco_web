# -*- coding: utf-8 -*-
from collections import Counter
import jieba
import jieba.posseg as pseg
import re
import sys
import json
import jieba.analyse
class KeywordExtractor:
    def __init__(self):
        jieba.set_dictionary('dict.txt.big')
        jieba.load_userdict('user_dict.txt')
        jieba.analyse.set_stop_words('stop_words.txt')
        self.stop_words = open('stop_words.txt', 'r').read().splitlines()
        jieba.initialize()

    def get_keywords(self, content):
        content = content.replace(" ","")
        return jieba.analyse.extract_tags(content, topK=7, withWeight=False, allowPOS=("nr", "nr", "nz", "nt", "n"))

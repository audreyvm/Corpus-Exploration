# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 09:02:26 2022

@author: Audrey
"""

from nltk.corpus.reader.bnc import BNCCorpusReader as bnc
import en_core_web_sm
import re
import collections

import Preprocessor as pp
nlp = en_core_web_sm.load()

bnc_reader = bnc(root="BNC/Texts", fileids=r'[A-K]/\w*/\w*\.xml')

full_adj_list = []   
    
for fileid in bnc_reader.fileids():
    file_root = pp.get_root(fileid)
    for s in file_root.iter('s'):
        for w in s.iter('w'):
            if w.get('pos') == 'ADJ' and re.search ('.*(al|ary|an|ical|ic)$', w.text):
                full_adj_list.append(w.text)
                    


counts = collections.Counter(full_adj_list)
common_adjs = [adj for adj, c in counts.items() if c>=30]


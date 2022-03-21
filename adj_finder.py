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

rel_adj_list = []   
qual_adj_list = []
    
for fileid in bnc_reader.fileids():
    file_root = pp.get_root(fileid)
    for s in file_root.iter('s'):
        for w in s.iter('w'):
            if w.get('pos') == 'ADJ' and re.search ('.*(al|ary|an|ic)$', w.text):
                rel_adj_list.append(w.text.lower())
            elif w.get('pos') == 'ADJ':
                qual_adj_list.append(w.text.lower())
                    


rel_counts = collections.Counter(rel_adj_list)
common_rel_adjs = [adj for adj, c in rel_counts.items() if c>=30]
rel_100=[adj for adj, c in rel_counts.most_common(100)]

qual_counts = collections.Counter(qual_adj_list)
qual_100=[adj for adj, c in qual_counts.most_common(100)]

al_list = []
ary_list = []
an_list = []
ical_list = []
ic_list = []

for adj in common_rel_adjs:
    if re.search('.*al$', adj):
        al_list.append(adj)
    elif re.search('.*ary$', adj):
        ary_list.append(adj)
    elif re.search('.*an$', adj):
        an_list.append(adj)
    elif re.search('.*ic$', adj):
        ic_list.append(adj)        

with open('adjectives.txt', 'w') as f:
    for item in ic_list:
        f.write("%s\n" % item)
        
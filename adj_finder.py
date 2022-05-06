# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 09:02:26 2022

@author: Audrey
"""

from nltk.corpus.reader.bnc import BNCCorpusReader as bnc
import re
import collections
import pandas as pd
import Preprocessor as pp
from tqdm import tqdm


bnc_reader = bnc(root="BNC/Texts", fileids=r'[A-K]/\w*/\w*\.xml')

rel_adj_list = []   
qual_adj_list = []

count = 0    
for fileid in tqdm(bnc_reader.fileids()):
    file_root = pp.get_root(fileid)
    for s in file_root.iter('s'):
        for w in s.iter('w'):
            if w.get('pos') == 'ADJ' and re.search ('.*(al|ary|an|ic)$', w.text.strip()):
                rel_adj_list.append(w.text.lower())

                    


rel_counts = collections.Counter(rel_adj_list)
full_rel_adjs =[adj for adj, c in rel_counts.items()]
common_rel_adjs = [adj for adj, c in rel_counts.items() if c>=30]
unique_rel_adjs = [adj for adj, c in rel_counts.items() if c==1]
rel_150=[adj for adj, c in rel_counts.most_common(150)]



adjs = pd.DataFrame(rel_150)
adjs.to_csv('adj_list.csv')

  

with open('adjectives.txt', 'w') as f:
    for item in al_list:
        f.write("%s\n" % item)
  
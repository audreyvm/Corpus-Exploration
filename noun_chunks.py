# -*- coding: utf-8 -*-
"""
Created on Tue May 10 18:49:46 2022

@author: Audrey
"""

import pandas as pd
import re
from tqdm import tqdm

corpus = pd.read_csv('Corpus.csv')


target_adj = [target for target in corpus['Target Adj']]
pos_lists = [pos_list.split(',') for pos_list in corpus['POS']]
sentence_list = [sentence.split() for sentence in corpus['Words']]

bare_nps = []    
count = 0
for target, sentence, pos_list in tqdm(zip(target_adj, sentence_list, pos_lists)):
    count += 1
    if count <= 10: 
        for i, (word, pos) in enumerate(zip( sentence, pos_list)):
            if word == target:
                print(word)
                noun_chunk = str(pos_list[i-3:i])
                print(noun_chunk)
                if re.search('DT', noun_chunk):
                    x = 'Has Determiner'
                else:
                    x = 'Bare'
        print(x)
        bare_nps.append(x)
        

corpus['Bare_in_PP'] = bare_nps

corpus.to_csv('Corpus.csv')


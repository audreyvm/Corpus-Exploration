# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:16:06 2022

@author: Audrey
"""

import pandas as pd
corpus = pd.read_csv('Corpus.csv')
data =  pd.read_csv('Ratings Concreteness.csv', sep = ';')
data = data[['Word', 'Conc.M']]

words = data['Word'].to_list()

hwconcrete = []
pphwconcrete = []
hwconcrete = [data.loc[data['Word'] == hw, 'Conc.M'].item() if str(hw) in words else 'N/A' for hw in corpus['Head word']]
pphwconcrete = [data.loc[data['Word'] == pphw, 'Conc.M'].item() if str(pphw) in words else 'N/A' for pphw in corpus['PP_Head_text']]
for hw, pphw in zip(corpus['Head word'], corpus['PP_Head_text']):
    if str(hw) in words:
        hwconcrete.append(data.loc[data['Word'] == hw, 'Conc.M'].item())
    else: hwconcrete.append('N/A')
    if str(pphw) in words:
        pphwconcrete.append(data.loc[data['Word'] == pphw, 'Conc.M'].item())
    else: pphwconcrete.append('N/A')
        
corpus['HW_Concreteness']= hwconcrete
corpus['PP_HW_Concreteness']= pphwconcrete

corpus.to_csv('Corpus.csv')

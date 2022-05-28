# -*- coding: utf-8 -*-
"""
Created on Mon May 23 19:47:58 2022

@author: Audrey
"""
import numpy as np
from scipy.stats import entropy
import pandas as pd
from tqdm import tqdm

corpus = pd.read_csv('Corpus.csv')
adj_data = pd.read_csv('Data_by_Adj_2.csv')
adjs = pd.read_csv('Adjective_list_15.5.csv',sep=';')
rel_list = [x for x in adjs['Relational'] if str(x)!= 'nan']
qual_list = [x for x in adjs['Qualitative'] if str(x)!= 'nan']
all_list = rel_list + qual_list

def entropy1(labels, base=None):
  value,counts = np.unique(labels, return_counts=True)
  return entropy(counts, base=base)

prep_entropy_list = []
hw_entropy_list = []
pphw_entropy_list = []
for adj in tqdm(all_list):
    prep_list = []
    hw_list = []
    pphw_list = []
    for target, hw, prep, pp_head, pph_text in zip(corpus['Target Adj'], corpus['Head word']
                                                   ,corpus['Prep'], corpus['PP_Head_POS'], corpus['PP_Head_text']):
        if target == adj and (pp_head == 'NOUN' or pp_head == 'PROPN'):
            hw_list.append(hw)
            if prep != 'N/A':
                prep_list.append(prep)
                pphw_list.append(pph_text)
    prep_entropies = entropy1(prep_list)
    hw_entropies = entropy1(hw_list)
    pphw_entropies = entropy1(pphw_list)
    prep_entropy_list.append(prep_entropies)
    hw_entropy_list.append(hw_entropies)
    pphw_entropy_list.append(pphw_entropies)
    
            
adj_data['Prep_Entropies'] = prep_entropy_list
adj_data['HW_Entropies'] = hw_entropy_list
adj_data['PP_HW_Entropies'] = pphw_entropy_list

adj_data.to_csv('Data_by_Adj_2.csv')

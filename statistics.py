# -*- coding: utf-8 -*-
"""
Created on Sat May  7 11:23:01 2022

@author: Audrey
"""
import pandas as pd
from tqdm import tqdm
import numpy as np
from scipy.stats import entropy
import re

corpus = pd.read_csv('Corpus.csv')
adjs = pd.read_csv('Adjective_list_15.5.csv',sep=';')
rel_list = [x for x in adjs['Relational'] if str(x)!= 'nan']
qual_list = [x for x in adjs['Qualitative'] if str(x)!= 'nan']
all_list = rel_list + qual_list

total = []
pp = []
nmod = []
adj_type = []
PP_bare_list = []
PP_bare_sing = []
PP_bare_pl = []
all_bare_sing = []
all_bare_pl = []
PP_in_NP = []
PP_in_VP = []
PP_in_AP = []
for adj in tqdm(all_list):
    if adj in rel_list:
        adj_type.append('Relational')
    else: adj_type.append('Qualitative')
    totalcount = 0
    ppcount = 0
    nmodcount = 0
    PP_bare_scount = 0
    PP_bare_plcount = 0        
    all_bare_scount = 0
    all_bare_plcount = 0
    PP_NP_count = 0
    PP_VP_count = 0
    PP_AP_count = 0
    for target, typ, bare, pp_head, head in zip(corpus['Target Adj'],corpus['Type'],
                                             corpus['Bare_NPs'], corpus['PP_Head_POS'], corpus['Head Word POS']):
        if target == adj:
            totalcount += 1
            if bare == 'Bare' and (head == 'NN' or head == 'NNP'): #this is pulling out bare pp heads, need the nouns - revisit!
                all_bare_scount += 1
            elif bare == 'Bare' and (head == 'NNS' or head == 'NNPS'):
                all_bare_plcount += 1
            if typ == 'PP':
                ppcount +=1
                if bare == 'Bare' and (head == 'NN' or head == 'NNP'): #this is pulling out bare pp heads, need the nouns - revisit!
                    PP_bare_scount += 1
                elif bare == 'Bare' and (head == 'NNS' or head == 'NNPS'):
                    PP_bare_plcount += 1
                if re.match('^NN*', str(pp_head)):
                #pp_head == 'NN' or pp_head == 'NNP' or pp_head == 'NNS' or pp_head == 'NNPS':
                    PP_NP_count += 1
                elif re.match('^V+', str(pp_head)):
                #pp_head == 'VB':
                    PP_VP_count += 1
                elif re.match('JJ*', str(pp_head)):
                    PP_AP_count +=1
            if typ == 'Noun_Modifier':
                nmodcount += 1
    total.append(totalcount)
    pp.append(ppcount)
    nmod.append(nmodcount)
    PP_bare_sing.append(PP_bare_scount)
    PP_bare_pl.append(PP_bare_plcount)
    all_bare_sing.append(all_bare_scount)
    all_bare_pl.append(all_bare_plcount)
    PP_in_NP.append(PP_NP_count)
    PP_in_AP.append(PP_AP_count)
    PP_in_VP.append(PP_VP_count)

lst_tuples = list(zip(all_list,adj_type, total, pp, nmod,PP_bare_sing, PP_bare_pl,all_bare_sing,all_bare_pl,PP_in_NP,
                      PP_in_VP, PP_in_AP))
data = pd.DataFrame(lst_tuples, columns = ['Adjective','Adj_Type', 'Count','PP',
                                          'NMod', 'Bare_in_PP_Sing', 'Bare_in_PP_Pl',
                                          'Bare_in_NP_Sing', 'Bare_in_NP_Pl','PP_in_NP','PP_in_VP','PP_in_AP'])

#convert the data to percentagess
data['PP_Percent'] = (data['PP']/data['Count'])
data['NMod'] = (data['NMod']/data['Count'])

data['Bare_in_PP_Pl'] = (data['Bare_in_PP_Pl']/data['PP'])
data['Bare_in_PP_Sing'] = (data['Bare_in_PP_Sing']/data['PP'])
data['Bare_in_NP_Pl'] = (data['Bare_in_NP_Pl']/data['Count'])
data['Bare_in_NP_Sing'] = (data['Bare_in_NP_Sing']/data['Count'])


data['PP_in_NP'] = (data['PP_in_NP']/data['PP'])
data['PP_in_VP'] = (data['PP_in_VP']/data['PP'])
data['PP_in_AP'] = (data['PP_in_AP']/data['PP'])


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
        if target == adj and re.match('^NN*', str(pp_head)):
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
    
            
data['Prep_Entropies'] = prep_entropy_list
data['HW_Entropies'] = hw_entropy_list
data['PP_HW_Entropies'] = pphw_entropy_list


data = data[data.Count != 0]
data.to_csv('Data_by_Adj_2.csv')





# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:20:33 2022

@author: Audrey
"""
from nltk.corpus.reader.bnc import BNCCorpusReader as bnc
import pandas as pd
import en_core_web_sm
import Preprocessor as pp
from tqdm import tqdm
import re
nlp = en_core_web_sm.load()

bnc_reader = bnc(root="BNC/Texts", fileids=r'[A-K]/\w*/\w*\.xml')
adjs = pd.read_csv('Adjective_list.csv',sep=';')
rel_list = [x for x in adjs['Relational'] if str(x)!= 'nan']
qual_list = [x for x in adjs['Qualitative'] if str(x)!= 'nan']
all_list = rel_list + qual_list

lemmas_lst = []
words_lst = []
id_lst = []
target_lst = []
adj_type_lst =[]
pos_lst = []
headnoun_lst=[]
prep_lst=[]
type_lst = []

pattern = str('|'.join(all_list))


for fileid in tqdm(bnc_reader.fileids()):
        file_root = pp.get_root(fileid)
        for s in file_root.iter('s'):
            sent_id, lemmas, words = pp.process_sentence(s, file_root)
            if re.search(pattern, words):      
                txt = nlp(words)
                for token in txt:
                    if token.text in all_list and token.pos_ == 'ADJ':
                        if token.text in rel_list:
                            adj_type_lst.append('Relational')
                        else: 
                            adj_type_lst.append('Qualitative')
                        x = token.head                         
                        target = token.text
                        pos = pp.pos_string(txt)
                        headnoun_lst.append(token.head.text)
                        if x.head.pos_ == 'ADP':
                            prep_lst.append(x.head.text)
                        else:
                            prep_lst.append('N/A')
                        target_lst.append(target)
                        pos_lst.append(pos)
                        if  x.pos_ == 'NOUN' and x.dep_ == 'pobj':
                            type_lst.append('PP')
                        elif x.pos_ == 'VERB':
                            type_lst.append('Predicate')
                        elif x.pos_ == 'NOUN':
                            type_lst.append('Modifier')
                        else: 
                            type_lst.append('Other')
                        lemmas_lst.append(lemmas)
                        words_lst.append(words)
                        file_id = fileid
                        new_id = sent_id + ' ' + file_id[5:8]
                        id_lst.append(new_id)

print('creating database')


lst_tuples = list(zip(id_lst,headnoun_lst,target_lst,adj_type_lst,type_lst,prep_lst,pos_lst, words_lst, lemmas_lst))
data = pd.DataFrame(lst_tuples, columns=['ID','Head word','Target Adj','Adj_Type','Type','Prep','POS','Words','Lemmas'])
data = data.sort_values(by=['Adj_Type', 'Type'])
print('Dataframe created')

relPP = ((data['Adj_Type'] == 'Relational') & (data['Type'] == 'PP')).sum()
relMOD = ((data['Adj_Type'] == 'Relational') & (data['Type'] == 'Modifier')).sum()
qualPP = ((data['Adj_Type'] == 'Qualitative') & (data['Type'] == 'PP')).sum()
qualMOD = ((data['Adj_Type'] == 'Qualitative') & (data['Type'] == 'Modifier')).sum()

relPPpercent = relPP/(relPP+relMOD)
print(relPPpercent)
qualPPpercent = qualPP/(qualPP+qualMOD)
print(qualPPpercent)

data.to_csv('Adjective_data.csv')
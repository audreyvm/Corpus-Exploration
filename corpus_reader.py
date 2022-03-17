# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:20:33 2022

@author: Audrey
"""

from nltk.corpus.reader.bnc import BNCCorpusReader as bnc
import pandas as pd
import en_core_web_sm
import Preprocessor as pp
nlp = en_core_web_sm.load()

bnc_reader = bnc(root="BNC/Texts", fileids=r'[A-K]/\w*/\w*\.xml')
adjs = pd.read_csv('Adjective_list.csv',sep=';')
all_list =adjs['All'].tolist()
rel_list =adjs['Relational'].tolist()
#poly_list =adjs['Polysemous'].tolist()
qual_list =adjs['Qualitative'].tolist()

adj_type = []
lemmas_lst = []
words_lst = []
target_lst = []
pos_lst = []
id_lst = []
headnoun_lst=[]
prep_lst=[]
type_lst = []


count = 0        
for fileid in bnc_reader.fileids():
    count += 1
    if count < 2:
        file_root = pp.get_root(fileid)
        for s in file_root.iter('s'):
            sent_id, lemmas, words = pp.process_sentence(s, file_root)
            if pp.has_target(words) == True:
                print(sent_id)
                txt = nlp(words)
                for token in txt:
                    if token.text in all_list and token.pos_ == 'ADJ':
                        x = token.head
                        if token.text in rel_list:
                            adj_type.append('Relational')
                        # if token.text in poly_list:
                        #     adj_type.append('Polysemous')
                        if token.text in qual_list:
                            adj_type.append('Qualitative')                            
                        target = pp.get_target(words)
                        pos = pp.pos_string(words)
                        file_id = fileid
                        new_id = sent_id + ' ' + file_id[5:8]
                        headnoun_lst.append(token.head.text)
                        if x.head.pos_ == 'ADP':
                            prep_lst.append(x.head.text)
                        else:
                            prep_lst.append('N/A')
                        lemmas_lst.append(lemmas)
                        words_lst.append(words)
                        target_lst.append(target)
                        pos_lst.append(pos)
                        id_lst.append(new_id)
                        if  x.pos_ == 'NOUN' and x.dep_ == 'pobj':
                            type_lst.append('PP')
                        elif x.pos_ == 'VERB':
                            type_lst.append('Predicate')
                        elif x.pos_ == 'NOUN':
                            type_lst.append('Modifier')
                        else: 
                            type_lst.append('Other')  
    

print('creating database')
print('Scanned ', count, 'files.')
lst_tuples = list(zip(id_lst,adj_type, target_lst,headnoun_lst, prep_lst, pos_lst, lemmas_lst, words_lst, type_lst))
data = pd.DataFrame(lst_tuples, columns=['ID', 'Adjective Type', 'Target Adj','Head word', 'Prep','POS','Lemmas', 'Words', 'Type'])
data = data.sort_values(by=['Adjective Type', 'Type'])
print('Dataframe created')

relPP = ((data['Adjective Type'] == 'Relational') & (data['Type'] == 'PP')).sum()
relMOD = ((data['Adjective Type'] == 'Relational') & (data['Type'] == 'Modifier')).sum()
qualPP = ((data['Adjective Type'] == 'Qualitative') & (data['Type'] == 'PP')).sum()
qualMOD = ((data['Adjective Type'] == 'Qualitative') & (data['Type'] == 'Modifier')).sum()
# polyPP = ((data['Adjective Type'] == 'Polysemous') & (data['Type'] == 'PP')).sum()
# polyMOD = ((data['Adjective Type'] == 'Polysemous') & (data['Type'] == 'Modifier')).sum()

relPPpercent = relPP/(relPP+relMOD)
print(relPPpercent)
qualPPpercent = qualPP/(qualPP+qualMOD)
print(qualPPpercent)
# polyPPpercent = polyPP/(polyPP+polyMOD)
# print(polyPPpercent)

data.to_csv('Adjective_data.csv')
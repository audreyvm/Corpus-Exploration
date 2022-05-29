# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:20:33 2022

@author: Audrey
"""
from nltk.corpus.reader.bnc import BNCCorpusReader as bnc
import pandas as pd
import en_core_web_sm
from tqdm import tqdm
import re
import xml.etree.ElementTree as ET
import os
nlp = en_core_web_sm.load()

bnc_reader = bnc(root="BNC/Texts", fileids=r'[A-K]/\w*/\w*\.xml')
adjs = pd.read_csv('Adjective_list_15.5.csv',sep=';')
rel_list = [x for x in adjs['Relational'] if str(x)!= 'nan']
qual_list = [x for x in adjs['Qualitative'] if str(x)!= 'nan']
all_list = rel_list + qual_list

def get_root(fileid):
    filename=os.path.join('','BNC','Texts',fileid)
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

def get_sentence(sentence):
    sent = []
    for child in sentence.iter('w'):
        if child.text is None: 
            continue
        else:
            sent.append(child.text)
    return sent

def make_strings(sentence):
    words = [word.lower().strip() for word in sentence]
    words_string =" ".join(words)
    return  words_string

def process_sentence(sentence, fileroot):
    sent_id = sentence.get('n')
    words = get_sentence(sentence)
    words = make_strings(words)
    return sent_id, words

def pos_string(spacey_obj):
    pos_lst = []
    for token in spacey_obj:
        x = token.tag_
        x = str(x)
        pos_lst.append(x)
    return pos_lst

lemmas_lst = []
words_lst = []
id_lst = []
target_lst = []
adj_type_lst =[]
pos_lst = []
headnoun_lst=[]
headnoun_pos_lst =[]
prep_lst=[]
PP_Head_POS = []
PP_Head_text = []
type_lst = []


pattern = str('|'.join(all_list))

for fileid in tqdm(bnc_reader.fileids()):
        file_root = get_root(fileid)
        for s in file_root.iter('s'):
            sent_id, words = process_sentence(s, file_root)
            if re.search(pattern, words):      
                txt = nlp(words)
                for token in txt:
                    if token.text in all_list and token.tag_ == 'JJ':
                        if token.text in rel_list:
                            adj_type_lst.append('Relational')
                        else: 
                            adj_type_lst.append('Qualitative')
                        x = token.head                         
                        target = token.text
                        pos = pos_string(txt)
                        headnoun_lst.append(token.head.text)
                        headnoun_pos_lst.append(token.head.tag_)
                        if x.head.pos_ == 'ADP':
                            prep_lst.append(x.head.text)
                            y = x.head
                            PP_Head_POS.append(y.head.tag_)
                            PP_Head_text.append(y.head.text)
                        else:
                            prep_lst.append('N/A')
                            PP_Head_POS.append('N/A')
                            PP_Head_text.append('N/A')
                        target_lst.append(target)
                        pos_lst.append(pos)
                        if  (x.pos_ == 'NOUN' or x.pos_ == 'PROPN') and x.dep_ == 'pobj':
                            type_lst.append('PP')
                        elif x.pos_ == 'VERB' or x.pos_ == 'AUX':
                            type_lst.append('Predicate')
                        elif (x.pos_ == 'NOUN' or x.pos_ == 'PROPN') and x.dep_ == 'compound':
                            type_lst.append('Noun_Modifier')
                        elif x.pos_ == 'NOUN' or x.pos_ == 'PROPN':
                            type_lst.append('Modifier')                            
                        else: 
                            type_lst.append('Other')
                        words_lst.append(words)
                        file_id = fileid
                        new_id = sent_id + ' ' + file_id[5:8]
                        id_lst.append(new_id)

print('creating database')


lst_tuples = list(zip(id_lst,headnoun_lst,headnoun_pos_lst ,target_lst,adj_type_lst,type_lst,prep_lst,PP_Head_POS, PP_Head_text, pos_lst, words_lst))
data = pd.DataFrame(lst_tuples, columns=['ID','Head word','Head Word POS', 'Target Adj','Adj_Type','Type','Prep','PP_Head_POS', 'PP_Head_text', 'POS','Words'])
print('Dataframe created')


print('Checking for bare NPs')
#target_adj = [target for target in data['Target Adj']]
sentence_list = [sentence.split() for sentence in data['Words']]

bare_nps = []    
for target, sentence, pos_list in tqdm(zip(target_lst, sentence_list, data['POS'])):
        for i, (word, pos) in enumerate(zip( sentence, pos_list)):
            if word == target:
                noun_chunk = str(pos_list[i-2:i])
                if re.search('DT', noun_chunk):
                    x = 'Has Determiner'
                else:
                    x = 'Bare'
        bare_nps.append(x)

    
data['Bare_NPs'] = bare_nps

print('Getting Noun Concreteness')
concrete =  pd.read_csv('Ratings Concreteness.csv', sep = ';')
concrete = concrete[['Word', 'Conc.M']]
words = concrete['Word'].to_list()

hwconcrete = [concrete.loc[concrete['Word'] == hw, 'Conc.M'].item() if str(hw) in words 
              else 'N/A' for hw in data['Head word']]
pphwconcrete = [concrete.loc[concrete['Word'] == pphw, 'Conc.M'].item() if str(pphw) in words 
                else 'N/A' for pphw in data['PP_Head_text']]

data['HW Concreteness'] = hwconcrete
data['PP HW Concreteness'] = pphwconcrete

data.to_csv('Corpus.csv')

# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:20:33 2022

@author: Audrey
"""

from nltk.corpus.reader.bnc import BNCCorpusReader as bnc
import pandas as pd
import xml.etree.ElementTree as ET
import os
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

bnc_reader = bnc(root="BNC/Texts", fileids=r'[A-K]/\w*/\w*\.xml')
adjs = pd.read_csv('Adjective_list.csv',sep=';')
all_list =adjs['All'].tolist()
rel_list =adjs['Relational'].tolist()
poly_list =adjs['Polysemous'].tolist()
qual_list =adjs['Qualitative'].tolist()


#makes it iterable with element tree
def get_root(fileid):
    filename=os.path.join('','BNC','Texts',fileid)
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

#turns the sentence into a list of lemma/word tuples
def get_sentence(tree_root):
    sentence = []
    for w in s.iter('w'):
            lemma = w.get('hw')
            word = w.text.lower()
            word_tuple = lemma, word
            sentence.append(word_tuple)
    return sentence

#turns lemma/word tuples into strings 
def make_strings(sentence):
    lemmas = [i[0] for i in sentence]
    words = [i[1] for i in sentence]
    words = [word.rstrip() for word in words]
    words_string =" ".join(words)
    words_string = words_string.lower()
    lemmas_string =" ".join(lemmas)
    return lemmas_string, words_string

#checks for presence of target word
def has_target(string):
    txt = nlp(string)
    count = 0
    for token in txt:
        if token.text in all_list and token.pos_ == 'ADJ':
            count +=1
        else: continue
    if count == 0:
        return False
    else: return True
        
#returns list of target words
def get_target(string):
    txt = nlp(string)
    for token in txt:
        if token.text in all_list and token.pos_ == 'ADJ':
            return token.text

#for all sentences not only with target words - need to figure this out
def pos_string(string):
    pos_lst = []
    txt = nlp(string)
    for token in txt:
        x = token.pos_
        x = str(x)
        pos_lst.append(x)
    return pos_lst
                    

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
    if count <=30:
        file_root = get_root(fileid)
        for s in file_root.iter('s'):
            tuples = get_sentence(file_root)
            lemmas, words = make_strings(tuples)
            sent_id = s.get('n')
            if has_target(words) == True:
                txt = nlp(words)
                for token in txt:
                    if token.text in all_list and token.pos_ == 'ADJ':
                        x = token.head
                        if token.text in rel_list:
                            adj_type.append('Relational')
                        if token.text in poly_list:
                            adj_type.append('Polysemous')
                        if token.text in qual_list:
                            adj_type.append('Qualitative')                            
                        target = get_target(words)
                        pos = pos_string(words)
                        file_id = fileid
                        new_id = sent_id + ' ' + file_id[5:8]
                        headnoun_lst.append(token.head.text)
                        prep_lst.append(x.head.text)
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
        
    else: break
print('creating database')
lst_tuples = list(zip(id_lst,adj_type, target_lst,headnoun_lst, prep_lst, pos_lst, lemmas_lst, words_lst, type_lst))
data = pd.DataFrame(lst_tuples, columns=['ID', 'Adjective Type', 'Target Adj','Head word', 'Prep','POS','Lemmas', 'Words', 'Type'])
data = data.sort_values(by=['Adjective Type', 'Type'])
print('Dataframe created')

relPP = ((data['Adjective Type'] == 'Relational') & (data['Type'] == 'PP')).sum()
relMOD = ((data['Adjective Type'] == 'Relational') & (data['Type'] == 'Modifier')).sum()
qualPP = ((data['Adjective Type'] == 'Qualitative') & (data['Type'] == 'PP')).sum()
qualMOD = ((data['Adjective Type'] == 'Qualitative') & (data['Type'] == 'Modifier')).sum()
polyPP = ((data['Adjective Type'] == 'Polysemous') & (data['Type'] == 'PP')).sum()
polyMOD = ((data['Adjective Type'] == 'Polysemous') & (data['Type'] == 'Modifier')).sum()

relPPpercent = relPP/(relPP+relMOD)
print(relPPpercent)
qualPPpercent = qualPP/(qualPP+qualMOD)
print(qualPPpercent)
polyPPpercent = polyPP/(polyPP+polyMOD)
print(polyPPpercent)
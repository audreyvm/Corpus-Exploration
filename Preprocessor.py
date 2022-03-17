# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 10:53:33 2022

@author: Audrey
"""

import pandas as pd
import xml.etree.ElementTree as ET
import os
import en_core_web_sm

nlp = en_core_web_sm.load()

adjs = pd.read_csv('Adjective_list.csv',sep=';')
all_list =adjs['All'].tolist()



#makes it iterable with element tree
def get_root(fileid):
    filename=os.path.join('','BNC','Texts',fileid)
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

#turns the sentence into a list of lemma/word tuples
def get_sentence(tree_root, sentence):
    s = []
    for w in sentence.iter('w'):
            lemma = w.get('hw')
            word = w.text.lower()
            word_tuple = lemma, word
            s.append(word_tuple)
    return s

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
                    
def process_sentence(sentence, fileroot):
    sent_id = sentence.get('n')
    tuples = get_sentence(fileroot, sentence)
    lemmas, words = make_strings(tuples)
    return sent_id,lemmas, words

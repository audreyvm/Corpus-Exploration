# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 10:53:33 2022

@author: Audrey
"""

import pandas as pd
import xml.etree.ElementTree as ET
import os


adjs = pd.read_csv('Adjective_list.csv',sep=';')
rel_list = [x for x in adjs['Relational'] if str(x)!= 'nan']
qual_list = [x for x in adjs['Qualitative'] if str(x)!= 'nan']
all_list = rel_list + qual_list



#makes it iterable with element tree
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
            word = child.text.lower()
            sent.append(word.strip())
    return str(sent)



def make_strings(sentence):

    words = [i[1] for i in sentence]
    words = [word.strip() for word in words]
    words_string =" ".join(words)
    words_string = words_string.lower()
    return  words_string

#checks for presence of target word
def has_target(string):
    count = 0
    sentence = string.split()
    for word in sentence:
        if word in all_list:
            count +=1
        else: continue
    if count == 0:
        return False
    else: return True
    

def pos_string(spacey_obj):
    pos_lst = []
    for token in spacey_obj:
        x = token.tag_
        x = str(x)
        pos_lst.append(x)
    return pos_lst

                    
def process_sentence(sentence, fileroot):
    sent_id = sentence.get('n')
    words = get_sentence(sentence)
    words = make_strings
    return sent_id, words

from nltk.corpus.reader.bnc import BNCCorpusReader as bnc
import pandas as pd
import xml.etree.ElementTree as ET
import os
import re

bnc_reader = bnc(root="BNC/Texts", fileids=r'[A-K]/\w*/\w*\.xml')
adjs = pd.read_csv('Adjective_list.csv')
adj_list =adjs['Adjective'].tolist()

#makes it iterable with element tree
def get_root(fileid):
    filename=os.path.join('','BNC','Texts',fileid)
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

#turns the sentence into a list of first ID and then tuples
def get_sentence(tree_root):
    sentence = []
    sent_id = s.get('n')
    sentence.append(sent_id)
    for w in s.iter('w'):
            pos = w.get('c5')
            lemma = w.get('hw')
            word = w.text
            word_tuple = pos, lemma, word
            sentence.append(word_tuple)
    return sentence

 
#identifies use of adjective
def ident_type(sentence):
    pos = [i[0] for i in sentence [1:]]
    words = [i[2] for i in sentence [1:]]
    pos_string =" ".join(pos)
    words_string ="".join(words)
    pp_pattern = r'(PRP|PRF)\s(DT0|AT0\s)*(AVP\s)*(AJ0\s)+(NN1|NN2)' 
    mod_pattern = r".*(AJ0)+\s(NN1|NN2)"

    x = re.search(pp_pattern, pos_string)
    y = re.search(mod_pattern, pos_string)
    
    if x:
        print('\nIts a PP\n',words_string)
    elif y:
        print('\nIts a modifier\n',words_string)
    else: print('\nMust be a predicate\n', words_string)
    
    return pos_string, words_string

    
#gets target word
def get_target(sentence):
    pos = [i[0] for i in sentence [1:]]
    lemmas = [i[1] for i in sentence[1:]]
    words = [i[2] for i in sentence [1:]]
    for p, l, w in zip(pos,lemmas, words):
        if l in adj_list and p == 'AJ0':
            print(p,w)
            
# def get_head_noun(sentence):
#     pos = [i[0] for i in sentence [1:]]
#     words = [i[2] for i in sentence [1:]]    
#     ind = get_index(sentence)
#     for i in pos:
#         if index(i)>ind and pos == 'NN1' or pos == 'NN2':
            
    
tuple_list = []    
count = 0        
for fileid in bnc_reader.fileids():
    count += 1
    if count <=3:
        file_root = get_root(fileid)
        for s in file_root.iter('s'):
            for w in s.iter('w'):
                pos = w.get('c5')
                lemma = w.get('hw')
                if pos == 'AJ0' and lemma in adj_list:
                    tuples = get_sentence(file_root)
                    tuple_list.append(tuples)
                    
    else: break
count = 0
for sent in tuple_list:
    ident_type(sent)
    pos = [i[0] for i in sent[1:]]
    lemmas = [i[1] for i in sent[1:]]
    words = [i[2] for i in sent[1:]]
    for p, l, w in zip(pos,lemmas, words):
        if l in adj_list and p == 'AJ0':
            print(p,w)




from nltk.corpus.reader.bnc import BNCCorpusReader as bnc
import pandas as pd
import re
import xml.etree.ElementTree as ET
import os

bnc_reader = bnc(root="BNC/Texts", fileids=r'[A-K]/\w*/\w*\.xml')
adjs = pd.read_csv('Adjective_list.csv')
adj_list =adjs['Adjective'].tolist()


def get_root(fileid):
    filename=os.path.join('','BNC','Texts',fileid)
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

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

total_list = []    
count = 0        
for fileid in bnc_reader.fileids():
    count += 1
    if count <=5:
        file_root = get_root(fileid)
        for s in file_root.iter('s'):
            for w in s.iter('w'):
                pos = w.get('c5')
                lemma = w.get('hw')
                if pos == 'AJ0' and lemma in adj_list:
                    tuples = get_sentence(file_root)
                    print(tuples)
                    total_list.append(tuples)
    else: break

sentenceDB = pd.DataFrame(total_list).set_index([0])

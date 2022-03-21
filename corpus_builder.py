# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:01:36 2022

@author: Audrey
"""

from nltk.corpus.reader.bnc import BNCCorpusReader as bnc
import pandas as pd
import en_core_web_sm
import Preprocessor as pp
import re
from spacy.tokens import DocBin

nlp = en_core_web_sm.load()

bnc_reader = bnc(root="BNC/Texts", fileids=r'[A-K]/\w*/\w*\.xml')
reladjs = open("adjectives.txt", "r")
rel_adjs = [line.rstrip('\n') for line in reladjs.readlines() if line.strip() != '']

#rel_adjs = reladjs.readlines()

count = 0
sent_dict = {}

docs = []
for fileid in bnc_reader.fileids():
    count +=1
    if count == 6:
        file_root = pp.get_root(fileid)
        for s in file_root.iter('s'):
            sent_id = fileid[5:8] + '-' +s.get('n')
            for w in s.iter('w'):
                if w.text is None: 
                    continue
                elif w.text.lower() in rel_adjs and w.get('pos') == 'ADJ':
                   adj = w.text.lower()
                   sentence = ''.join(s.itertext())
                   values =[adj,sentence]
                   sent_dict[sent_id] = values

sentences = []
for adj, sentence in sent_dict.values():
    sentences.append(sentence)

doc_bin = DocBin()   
for doc in nlp.pipe(sentences):
    doc_bin.add(doc)
bytes_data = doc_bin.to_bytes()   
             

doc_bin.to_disk("./data.spacy")           
docbin_loaded = DocBin().from_disk(path = 'data.spacy')
docs_loaded = list(docbin_loaded.get_docs(nlp.vocab)) 
#corpus = pd.DataFrame.from_dict(sent_dict, orient='index', columns=['Adj', 'Text'])
#corpus.to_csv('minicorpus.csv', sep = ';')
                


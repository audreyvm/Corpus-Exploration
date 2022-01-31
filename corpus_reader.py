from nltk.corpus.reader.bnc import BNCCorpusReader as bnc
import pandas as pd
import re

bnc_reader = bnc(root="C:/Users/Audrey/OneDrive/Documents/Masters/Thesis/Corpus Exploration/BNC/Texts", fileids=r'[A-K]/\w*/\w*\.xml')
adjs = pd.read_csv('Adjective_list.csv')
adj_list =adjs['Adjective'].tolist()

filecount = 0
wordcount = 0
lst = []
for fileid in bnc_reader.fileids():
    if filecount <= 100:
        filecount += 1
        for sent in bnc_reader.tagged_sents(fileid):
            if wordcount <=100:
                wordcount+=1
                lst.append(sent)
            else: break
    
    else:break
    
sent_list = []
for sent in lst:
    for x in sent:
        if x[1] == 'ADJ' and x[0] in adj_list:
            sent_list.append(sent)

sent_string = str(sent_list)
#print(sent_string[0:500])
prep_phrase = r'\(\S+\s\'PREP\'\).+?\'ADJ\'\).+?\'SUBST\'\)'
          
for sent in sent_list:
    phrases = re.findall(prep_phrase, sent)        
#phrases = re.findall(prep_phrase, sent_string) 
print(phrases)   
    
            

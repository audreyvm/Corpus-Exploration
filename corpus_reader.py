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
    for w in s.iter('w'):
            pos = w.get('c5')
            lemma = w.get('hw')
            word = w.text
            word_tuple = pos, lemma, word
            sentence.append(word_tuple)
    return sentence

def make_strings(sentence):
    pos = [i[0] for i in sentence]
    lemmas = [i[1] for i in sentence]
    words = [i[2] for i in sentence]
    words = [word.rstrip() for word in words]
    pos_string =" ".join(pos)
    words_string =" ".join(words)
    lemmas_string =" ".join(lemmas)
    return pos_string, lemmas_string, words_string

#gets target word
def get_target(sentence):
    pos = [i[0] for i in sentence]
    lemmas = [i[1] for i in sentence]
    words = [i[2] for i in sentence]
    for p, l, w in zip(pos,lemmas, words):
        if l in adj_list and p == 'AJ0':
            return w                 
    
tuple_list = []
id_lst =[]    
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
                    sent_id = s.get('n')
                    file_id = fileid
                    new_id = sent_id + ' ' + file_id[5:8]
                    id_lst.append(new_id)
                    tuples = get_sentence(file_root)
                    tuple_list.append(tuples)                    
    else: break

pos_lst = []
lemmas_lst = []
words_lst = []
target_lst = []

for sent in tuple_list:
    pos, lemmas, words = make_strings(sent)
    target = get_target(sent)
    pos_lst.append(pos)
    lemmas_lst.append(lemmas)
    words_lst.append(words)
    target_lst.append(target)
    
    
lst_tuples = list(zip(id_lst, target_lst, pos_lst, lemmas_lst, words_lst))
data = pd.DataFrame(lst_tuples, columns=['ID', 'Target Adj', 'POS','Lemmas', 'Words'])
data = data.set_index('ID')
print('Dataframe created')
    
#identifies use of adjective
def ident_type(sentence):
    pos, lemmas, words = make_strings(sentence)
    pp_pattern = r'(PRP|PRF)\s(DT0|AT0\s)*(AVP\s)*(AJ0\s)+(NN1|NN2)' 
    mod_pattern = r".*(AJ0)+\s(NN1|NN2)"

    x = re.search(pp_pattern, pos)
    y = re.search(mod_pattern, pos)
    
    if x:
        print('\nIts a PP\n',words)
    elif y:
        print('\nIts a modifier\n',words)
    else: print('\nMust be a predicate\n', words)


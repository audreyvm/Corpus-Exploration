from nltk.corpus.reader.bnc import BNCCorpusReader as bnc
import pandas as pd
import xml.etree.ElementTree as ET
import os
import re
import spacy
from spacy import displacy

bnc_reader = bnc(root="BNC/Texts", fileids=r'[A-K]/\w*/\w*\.xml')
adjs = pd.read_csv('Adjective_list.csv')
adj_list =adjs['Adjective'].tolist()
nlp=spacy.load('en_core_web_sm')


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
        if token.text in adj_list and token.pos_ == 'ADJ':
            count +=1
        else: continue
    if count == 0:
        return False
    else: return True
        
#returns list of target words
def get_target(string):
    txt = nlp(string)
    for token in txt:
        if token.text in adj_list and token.pos_ == 'ADJ':
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
                
    
tuples_lst = []
lemmas_lst = []
words_lst = []
target_lst = []
pos_lst = []
id_lst = []
headnoun_lst=[]
type_lst=[]
count = 0        
for fileid in bnc_reader.fileids():
    count += 1
    if count <=1:
        file_root = get_root(fileid)
        for s in file_root.iter('s'):
            tuples = get_sentence(file_root)
            lemmas, words = make_strings(tuples)
            sent_id = s.get('n')
            if has_target(words) == True:
                tuples_lst.append(tuples)
                lemmas_lst.append(lemmas)
                words_lst.append(words)
                target = get_target(words)
                target_lst.append(target)
                pos = pos_string(words)
                pos_lst.append(pos)
                file_id = fileid
                new_id = sent_id + ' ' + file_id[5:8]
                id_lst.append(new_id)
                txt = nlp(words)
                for token in txt:
                    if token.text in adj_list and token.pos_ == 'ADJ':
                        headnoun_lst.append(token.head.text)
                    else: continue
                for token in txt:
                    x = token.head
                    if token.text in adj_list and token.pos_ == 'ADJ':
                            if x.head.dep_ == 'prep':
                                type_lst.append('PP')
                            else: type_lst.append('other')
    else: break
print('creating database')
lst_tuples = list(zip(id_lst, target_lst,headnoun_lst, pos_lst, lemmas_lst, words_lst, type_lst))
data = pd.DataFrame(lst_tuples, columns=['ID', 'Target Adj','Head Noun', 'POS','Lemmas', 'Words', 'Type'])
data = data.set_index('ID')
print('Dataframe created')


# for sent in tuple_list:
#     lemmas, words = make_strings(sent)
#     target = get_target(sent)
#     pos_lst.append(pos)
#     lemmas_lst.append(lemmas)
#     words_lst.append(words)
#     target_lst.append(target)
#     txt = nlp(words)




# sentence = words_lst[13]
# txt = nlp(sentence)
# for token in txt:
#     if token.text in adj_list and token.pos_ == 'ADJ':
#         print(token, token.pos_ ,token.dep_,token.head)



# # for string in words_lst:
# #     count += 1
# #     txt = nlp(string)
# #     if count <1:
# #         print(txt)
# #         for token in txt:
# #             print(token.text, token.head.text)
    
# # #identifies use of adjective
# # def ident_type(sentence):
# #     pos, lemmas, words = make_strings(sentence)
# #     pp_pattern = r'(PRP|PRF)\s(DT0|AT0\s)*(AVP\s)*(AJ0\s)+(NN1|NN2)' 
# #     mod_pattern = r".*(AJ0)+\s(NN1|NN2)"

# #     x = re.search(pp_pattern, pos)
# #     y = re.search(mod_pattern, pos)
    
# #     if x:
# #         print('\nIts a PP\n',words)
# #     elif y:
# #         print('\nIts a modifier\n',words)
# #     else: print('\nMust be a predicate\n', words)
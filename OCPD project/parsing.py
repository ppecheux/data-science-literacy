#%%
import os, os.path, pickle
from bs4 import BeautifulSoup
#%%
with open('article_name_dic.pickle','rb')as fp:
    dic_links = pickle.load(fp)

#%%
#link = next(iter(dic_links))
def get_txt_article(link='https://lungdiseasenews.com/2015/08/18/boehringer-ingelheims-spiolto-respimat-improves-quality-life-copd-patients/'):
    name = link.replace("/","")
    html = 'copd/article/'+ name+'.html'
    with open(html) as fp:
        soup = BeautifulSoup(fp)
    pf_content = soup.find("div",class_="pf-content").get_text()
    pf_content=pf_content.replace('Print This Article','')
    #print(pf_content)
    return pf_content
    #for readmorebox in soup.find_all("a",class_="readmore-link"):
    #print(pf_content.attrs['href'])
#get_txt_article()

#%%
def get_list_comments(link='https://lungdiseasenews.com/2017/09/15/lung-disease-study-identifies-a-type-of-regenerative-cell-and-a-type-of-scar-forming-one/'):
    name = link.replace("/","")
    html = 'copd/article/'+ name+'.html'
    with open(html) as fp:
        soup = BeautifulSoup(fp)
    try:
        comment_list = [content.get_text().replace('\n','').replace('\t','') for content in soup.findAll('div',class_='comment-content')]
        return comment_list
    except:
        return []
    #print(comment_list)
#get_list_comments()


#%%
import string
import numpy as np
from spacy.lang.en.stop_words import STOP_WORDS
import en_core_web_sm
from spacy.lang.en import English
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
nlp = en_core_web_sm.load()
parser = English()

#%%
# Creating our tokenizer function
def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = parser(sentence)

    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
    custom_stop_words = ['®']
    # Removing stop words and ponctuation
    mytokens = [ word for word in mytokens if word not in STOP_WORDS and word not in custom_stop_words and word not in string.punctuation ]

    # return preprocessed list of tokens
    return mytokens

#print(spacy_tokenizer(get_txt_article()))

#%%
#Create a list of tockenised sentences of all articles
def sentences_all_articles(dic_links= dic_links):
    pf_sentences = []
    for link in dic_links.keys():
        pf_sentences += get_txt_article(link).split('.')
    #print(pf_sentences)
    sentences = [spacy_tokenizer(sentence) for sentence in pf_sentences]
    return sentences
sentences = sentences_all_articles()
print(sentences)
#%%
#Save allarticle sentences
with open('sentences_all_article.pickle','wb+')as fp:
    pickle.dump(sentences,fp)

#%%
#Gives the vector of a word based on the nlp model that we choosed
doc = nlp(get_txt_article())
for tocken in doc[10:12]:
    print(tocken.vector)
    break
#%%
#
from gensim.models import word2vec

#%%
sentences = [spacy_tokenizer(sentence) for sentence in get_txt_article().split('.')]

#%%
with open('sentences_all_article.pickle','rb')as fp:
    sentences = pickle.load(fp)
print(sentences)

#%%
# gives the most similar words from copd
model = word2vec.Word2Vec(sentences, size=200)
print(sentences)
print(model.wv.vocab )
model.most_similar(['copd'])
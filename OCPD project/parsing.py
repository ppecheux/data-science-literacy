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
#DO NOT WORK
from numpy import dot
from numpy.linalg import norm
import scipy

# you can access known words from the parser's vocabulary
mytokens = spacy_tokenizer(get_txt_article())
nasa = parser.vocab['copd']


# cosine similarity
cosine = lambda v1, v2: dot(v1, v2) / (norm(v1) * norm(v2))

# gather all known words, take only the lowercased versions
allWords = list({w for w in parser.vocab if w.has_vector and w.orth_.islower() and w.lower_ != "copd"})
print(len(allWords))
# sort by similarity to NASA
allWords.sort(key=lambda w: cosine(w.vector, nasa.vector))
allWords.reverse()
print("Top 10 most similar words to copd:")
for word in allWords[:10]:   
    print(word.orth_)

#%%
#
#bow_vector = CountVectorizer(tokenizer = spacy_tokenizer, ngram_range=(1,1))

#%%
def cosine_distance_wordembedding_method(s1, s2):
    vector_1 = np.mean([word.has_vector for word in s1],axis=0)
    vector_2 = np.mean([word.has_wector for word in s2],axis=0)
    cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
    print('Word Embedding method with a cosine distance asses that our two sentences are similar to',round((1-cosine)*100,2),'%')
#tockens= spacy_tokenizer(get_txt_article())
#cosine_distance_wordembedding_method(tockens[:10],tockens[11:20])

#%%

doc = nlp(get_txt_article())
for tocken in doc[10:12]:
    print(tocken.vector)
    break
#%%
#
from gensim.models import word2vec

#%%
#sentences = word2vec.Text8Corpus('text8')
sentences = [spacy_tokenizer(sentence) for sentence in get_txt_article().split('.')]
#%%

model = word2vec.Word2Vec(sentences, size=200)
print(sentences)
print(model.wv.vocab )
model.most_similar(['copd'])
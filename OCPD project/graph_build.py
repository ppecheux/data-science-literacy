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
#
from gensim.models import word2vec

#%%
with open('sentences_all_article.pickle','rb')as fp:
    sentences = pickle.load(fp)
#print(sentences)
#%%
# gives the most similar words from copd
model = word2vec.Word2Vec(sentences, size=200)
#print(sentences)
print(model.wv.vocab )
model.most_similar(['copd'])

#%%
import networkx as nx
#%%
graph = nx.Graph()
graph.add_nodes_from(list(model.wv.vocab))
print(len(model.wv.vocab))
for word in model.wv.vocab:
    for s in model.most_similar(word):
        graph.add_edge(word,s[0],weigh = s[1])

#%%
print(nx.info(graph))

#%%
nx.write_gexf(graph,'article_vocab.gexf')

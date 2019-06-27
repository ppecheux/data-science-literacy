#%%
#
import numpy as np
import pickle

from gensim.models import word2vec

#%%
with open('sentences_all_article.pickle','rb')as fp:
    sentences = pickle.load(fp)
print(sentences)
#%%select only the nouns
from spacy.lang.en import English
import en_core_web_sm
nlp = spacy.load('en_core_web_sm')
parser = English()
#%%
def pos_filter(sentences = sentences,pos = "-NOUN-"):
    pos_sentences = []
    for sentence in sentences:
        #print(sentence)
        mytokens = nlp(' '.join(sentence))
        pos_sentence = [word.lemma_ for word in mytokens if word.pos_ == 'NOUN' ]
        pos_sentences.append(pos_sentence)
    print(pos_sentences)

noun_sentences = pos_filter(sentences)


#%%
# gives the most similar words from copd
model = word2vec.Word2Vec(sentences, size=200)
#print(sentences)
#print(model.wv.vocab )
print(model.wv.vocab["copd"].count)
#model.most_similar(['copd'])
#%%
from gensim.models import TfidfModel
from gensim import corpora

#%%
import networkx as nx
#%%
def build_similarity_graph(sentences = sentences):
    model = word2vec.Word2Vec(sentences, size=200)
    graph = nx.Graph()
    graph.add_nodes_from(list(model.wv.vocab))
    print(len(model.wv.vocab))
    for word in model.wv.vocab:
        for s in model.most_similar(word):
            graph.add_edge(word,s[0],weight = s[1])
    return graph


#%%
def build_noun_graph(sentences = sentences):
    model = word2vec.Word2Vec(sentences, size=200)
    graph = nx.Graph()
    graph.add_nodes_from(list(model.wv.vocab))
    print(len(model.wv.vocab))
    for word in model.wv.vocab:
        for s in model.most_similar(word):
            graph.add_edge(word,s[0],weight = s[1])
    return graph
#%%
graph = build_similarity_graph(sentences)
print(nx.info(graph))

#%%
nx.write_gexf(graph,'article_vocab.gexf')

#%%
with open('sentences_all_comments.pickle','rb')as fp:
    sentences = pickle.load(fp)
#print(sentences)
sentences = np.asarray(set(sentences))

#%%
graph = build_similarity_graph(sentences= sentences)
print(nx.info(graph))
#%%
nx.write_gexf(graph,'comments_vocab.gexf')



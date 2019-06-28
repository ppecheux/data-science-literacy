#%%
#
import pickle
from gensim.models import word2vec

#%%
with open('sentences_all_article.pickle','rb')as fp:
    sentences = pickle.load(fp)
print(sentences[:10])
#%%select only the nouns
import spacy
import en_core_web_sm
nlp = spacy.load('en_core_web_sm')
sentences = [['site', 'copd'], ['dwell', 'pulmonary', 'fibrosis']]

#%%
# selects the words with specific pos
def pos_filter(sentences = sentences,pos = ["NOUN"]):
    pos_sentences = []
    for sentence in sentences:
        #print(sentence)
        mytokens = nlp(' '.join(sentence))
        pos_sentence = [word.string.strip() for word in mytokens if word.pos_ is in pos ]
        pos_sentences.append(pos_sentence)
    print(pos_sentences)
    return pos_sentences

noun_sentences = pos_filter(sentences)
#%%
#Save all noun sentences in a list pickle
#
noun_string_sentences = []
for sentence in noun_sentences:
    noun_string_sentence = [word.string.strip() for word in sentence]
    noun_string_sentences.append(noun_string_sentence)

#%%
#
with open('noun_sentences.pickle','wb+')as fp:
    pickle.dump(noun_string_sentences,fp)
#%%
# gives the most similar words from copd
model = word2vec.Word2Vec(sentences, size=200, min_count=1)
#print(sentences)
#print(model.wv.vocab )
print(model.wv.vocab["copd"].count)
#model.most_similar(['copd'])


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
#
def build_list_nodes(sentences = sentences):
    freq_word_list = []
    model = word2vec.Word2Vec(sentences, size=200)

    for word in model.wv.vocab:
        t = (word,{'frequency':model.wv.vocab[word].count})
        freq_word_list.append(t)
    return freq_word_list, model
#%%
# build list of (word,{'freq':freq})
def build_weighted_graph(sentences = sentences):
    freq_word_list, model = build_list_nodes(sentences=sentences)
    print(freq_word_list[:10])
    graph = nx.Graph()
    graph.add_nodes_from(freq_word_list)
    print(len(model.wv.vocab))

    for word in model.wv.vocab:
        for s in model.most_similar(word):
            graph.add_edge(word,s[0],weight = s[1])
    return graph
#%%
graph = build_weighted_graph(sentences)
print(nx.info(graph))

#%%
nx.write_gexf(graph,'article_vocab.gexf')

#%%
#import numpy as np
with open('sentences_all_comments.pickle','rb')as fp:
    sentences = pickle.load(fp)
print(sentences)
#sentences = np.asarray(set(sentences))

#%%
graph_comments = build_weighted_graph(sentences= sentences)
print(nx.info(graph_comments))
#%%
nx.write_gexf(graph_comments,'comments_vocab.gexf')

#%%
with open('noun_sentences.pickle','rb')as fp:
    sentences = pickle.load(fp)
graph = build_weighted_graph(sentences= sentences)
print(nx.info(graph))

#%%
nx.write_gexf(graph,'noun_freq_articles.gexf')

#%%


#%%

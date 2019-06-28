#%%
import os, os.path, pickle
from bs4 import BeautifulSoup
#%%
# Open the dictionary that helps to find the file in the folder
with open('article_name_dic.pickle','rb')as fp:
    dic_links = pickle.load(fp)

#%%

def get_txt_article(link='https://lungdiseasenews.com/2015/08/18/boehringer-ingelheims-spiolto-respimat-improves-quality-life-copd-patients/'):
    name = link.replace("/","")
    html = 'copd/article/'+ name+'.html'
    with open(html) as fp:
        soup = BeautifulSoup(fp)
    pf_content = soup.find("div",class_="pf-content").get_text()
    pf_content=pf_content.replace('Print This Article','')
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
from spacy.lang.en.stop_words import STOP_WORDS
import en_core_web_sm
nlp = en_core_web_sm.load()
#nlp.max_length = 2000000

#%%
# Creating our tokenizer function
def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = nlp(sentence)

    # Lemmatizing each token and converting each token into lowercase
    # We also remove numbers
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens if word.lemma_ != "-NUM-"]

    custom_stop_words = ['®','“','”','’','']
    # Removing stop words and ponctuation
    mytokens = [ word for word in mytokens if word not in STOP_WORDS and word not in custom_stop_words and word not in string.punctuation and len(word)>0]

    # return preprocessed list of tokens
    return mytokens

#print(spacy_tokenizer(get_txt_article()))
#%%
# Create a list of tockenised sentences of all articles
def get_text_all_articles(dic_links= dic_links):
    pf_sentences_list = []
    for link in dic_links.keys():
        pf_sentences_list.append(get_txt_article(link))
        
    return(pf_sentences_list)
pf_sentences_list=get_text_all_articles()
#%%
print(len(pf_sentences_list))

#%%
# Divides the text document into a list of sentences using nlp
def doc_to_string(doc=['Devices that remotely monitor COPD patients’ conditions could help improve their outcomes, a study suggests.','\nA Cedars-Sinai Medical CenterÂ\xa0team said there were signs in the previous research it analyzed that remote monitoring could help COPD patients, although the evidence was far from definitive.\nIn addition, their analysis of 27 clinical trial results failed to provide enough evidence that the devices can improve the outcomes of patients with other conditions. Four of the trials the Los Angeles researchers looked at were for COPD.\nTheir report,Â\xa0â\x80\x9cImpact of remote patient monitoring on clinical outcomes: an updated meta-analysis of randomized controlled trials,Â\xa0appeared in the journal npj Digital Medicine.']):
    sentences = []
    count = 0
    for article in doc:
        print(count)
        count +=1
        tocken = nlp(article)
        sentences += [sent.string.strip() for sent in tocken.sents]
        
    return sentences
#print(len(doc_to_string()))
#%%
#Create a list of tockenised sentences of all articles
def sentences_all_articles(text_list = pf_sentences_list):
    pf_sentences = doc_to_string(doc = text_list)
    sentences = [spacy_tokenizer(sentence) for sentence in pf_sentences]
    return sentences
#sentences = sentences_all_articles()
#print(len(sentences))
#print(sentences[:10])
#%%
#Save allarticle sentences
with open('sentences_all_article.pickle','wb+')as fp:
    pickle.dump(sentences,fp)


#%%
# Get the list of sentences of the comment without the tockenization
def list_sentences_comments(dic_links=dic_links):
    all_comments = []
    joined_com = ''
    for link in dic_links.keys():
        comments = get_list_comments(link)
        joined_com = joined_com.join(comments)
        tocken = nlp(joined_com)
        comments = [sent.string.strip() for sent in tocken.sents]
        all_comments += comments

    print(all_comments)
#    commment_sentences = [spacy_tokenizer(sentence) for sentence in comments]
    return all_comments
comment_sentences = list_sentences_comments()
print(comment_sentences)


#%%
#Save all comment sentences in a list
list_sentences_comments = comment_sentences
with open('list_sentences_comments.pickle','wb+')as fp:
    pickle.dump(list_sentences_comments,fp)


#%%
# Verify what is inside sentences_all_comments : list of sentences tockenized
with open('sentences_all_comments.pickle','rb')as fp:
    com_sentences = pickle.load(fp)
print(com_sentences[:10])
#%%
import pickle
import re

#%%
#Search for the age of the people interested
with open('list_sentences_comments.pickle','rb')as fp:
    com_sentences = pickle.load(fp)
print(com_sentences[:10])
#%%
regex = r"\d{2}[[:blank:]][y]"

test_str = ''.join(com_sentences)
#print(test_str)
matches = re.finditer(regex, test_str, re.MULTILINE)
#print(len(matches))
for matchNum, match in enumerate(matches, start=1):
    print('i')
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

#%%
#
regex = r"([Ii]((\sam)|(\swas)|(’m))\s(((\w+\s+)?\d{2})|((\w+\s+)+?\d{2}\s[y])))"
regage = r"\d{2}"
unic_com_sentences = list(set(com_sentences))
test_str = ''.join(unic_com_sentences)
#print(test_str)
matches = re.finditer(regex, test_str, re.MULTILINE)
age = []
for matchNum, match in enumerate(matches, start=1):
    #print('i')
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    matches_ages = re.finditer(regage, match.group(), re.MULTILINE)
    for matchNum_age, match_age in enumerate(matches_ages, start=1):
        if int(match_age.group())>19:
            age.append(int(match_age.group()))
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

print(age)

#%%
#
import matplotlib.pyplot as plt

#%%
plt.hist(age,label='age in years')
#%%

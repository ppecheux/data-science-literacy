#%%
import random, time, pickle, requests, os, os.path

#%% [markdown]
## build of the url
def url_list_article(page = 1,category="copd"):
    return "https://lungdiseasenews.com/category/" + category + "/page/"+str(page)+"/"
print(url_list_article(page=4))

#%%
def download_list_articles(category = 'copd'):
    page = 0
    while(page<400):
        page+=1
        print('page '+str(page))
        try:
            if(os.stat(str(category) +'/lungnewslist'+ str(page)+'.html').st_size > 60000):
                continue
        except:
            pass
        if (page==1):
            r2 = requests.get("https://lungdiseasenews.com/category/" + category + "/",timeout = 5)
        else:
            r2 = requests.get(url_list_article(page=page,category=category),timeout = 5)
        time.sleep(random.random()*3)
        if(r2.status_code==requests.codes.ok):
            with open(str(category) +'/lungnewslist'+ str(page)+'.html','w+',encoding='utf-8') as fp:
                fp.write(r2.text)
        else:
            print('stop at page '+str(page))
            break
download_list_articles()
#%%
from bs4 import BeautifulSoup


#%% [markdown]
## find read more links
page = 2
category = 'copd'
html = str(category) +'/lungnewslist'+ str(page)+'.html'
with open(html) as fp:
    soup = BeautifulSoup(fp)
#print(soup.text)
for readmorebox in soup.find_all("a",class_="readmore-link"):
    print(readmorebox.attrs['href'])

#%%
def find_href_in_page(page=1,category='copd'):
    html = str(category) +'/lungnewslist'+ str(page)+'.html'
    with open(html) as fp:
        soup = BeautifulSoup(fp)
    #print(soup.text)
    hrefs = []
    for readmorebox in soup.find_all("a",class_="readmore-link"):
        hrefs.append(readmorebox.attrs['href'])
    return(hrefs)
#find_href_in_page()
#%%
def find_article_links(category='copd'):
    DIR = '/home/pier/Documents/P19/data science literacy/OCPD project/' + category
    #print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
    count_html=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    hrefs = []
    for page in range(1,count_html+1):
        links=find_href_in_page(page=page,category=category)
        #print("for "+str(page)+' we have '+str(len(links)))
        #print(links)
        hrefs+=links
    return hrefs

print(len(find_article_links()))
#%%
hrefs = find_article_links()
#print(hrefs)
with open('hrefs_ocpd_article.pickle','wb+')as fp:
    pickle.dump(hrefs,fp)

#%%
with open('hrefs_ocpd_article.pickle','rb')as fp:
    hrefslinks = pickle.load(fp)

#%%
hrefslinks



#%%
dic_links = {}
for link in hrefslinks:
    dic_links[link]='no'
#dic_links

#%%
def download_list_articles(links = hrefslinks):
    count=0
    for link in dic_links.keys():
        if(dic_links[link]=='no'):
            count+=1
            print(count)
            r = requests.get(link,timeout=4)
            time.sleep(0.5+random.random())
            if(r.status_code==requests.codes.ok and len(r.text)>500):
                dic_links[link]='done'
                name = link.replace("/","")
                with open('copd/article/'+ name+'.html','w+',encoding='utf-8') as fp:
                    fp.write(r.text)
download_list_articles()

#%%
dic_links

#%%
with open('article_name_dic.pickle','wb+')as fp:
    pickle.dump(dic_links,fp)

#%%
with open('article_name_dic.pickle','rb')as fp:
    dic_links = pickle.load(fp)

#%%
dic_names
#%%
import random, time, pickle, requests, os

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
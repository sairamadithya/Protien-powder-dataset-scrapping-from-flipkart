#!/usr/bin/env python
# coding: utf-8

# In[55]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[11]:


headers= { 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
  }
a=requests.get('https://www.flipkart.com/search?q=protein+powder',headers=headers)
print(a.status_code)


# In[12]:


soup=BeautifulSoup(a.content,'html.parser')


# In[96]:


price_l=[]
title_l=[]
weight_l=[]
flavour_l=[]
org_price_l=[]
views_l=[]
rating_l=[]
assured=[]
def extractinfo(webpage, page_number):
    next_page = webpage + '&page='+str(page_number)
    response= requests.get(str(next_page))
    soup = BeautifulSoup(response.content,"html.parser")
    price=soup.find_all('div',class_='_30jeq3')
    title=soup.find_all('a',class_='s1Q9rs')
    weight_flav=soup.find_all('div',class_='_3Djpdu')
    for a in weight_flav:
        weight=a.text[0:4]
        flav=a.text[6:]                       
    org_price=soup.find_all('div',class_='_3I9_wc')
    views=soup.find_all('span',class_='_2_R_DZ')[1:-1]
    rating=soup.find_all('div',class_='_3LWZlK')
    for b in views:
        if soup.find_all('div',class_='_32g5_j') is not None:
            assurance=True
            assured.append(assurance)
        elif soup.find_all('div',class_='_32g5_j') is None:
            assurance=False
            assured.append(assurance)
    for x in range(len(views)):
        price_l.append(price[x].text[1:])
        title_l.append(title[x].text)   
        weight_l.append(weight_flav[x].text[0:4])
        flavour_l.append(weight_flav[x].text[6:])
        org_price_l.append(org_price[x].text[1:])
        views_l.append(views[x].text[1:-1])
        rating_l.append(rating[x].text)
    if page_number < 25:
        page_number = page_number + 1
        extractinfo(webpage, page_number)
extractinfo('https://www.flipkart.com/search?q=protein+powder',0)
data = { 'Product name': title_l,'Product weight':weight_l, 'Product flavour':flavour_l, 'Views':views_l, 'Rating':rating_l,'Assurance':assured,'Original price':org_price_l,'Final price':price_l}
df = pd.DataFrame(data, columns = ['Product name','Product weight','Product flavour','Views','Rating','Assurance','Original price','Final price'])
df.to_csv('protien_powder_dataset_scrapped.csv')


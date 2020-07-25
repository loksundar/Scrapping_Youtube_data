# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 03:21:39 2020

@author: LOKSUNDAR
"""
from selenium import webdriver 
import pandas as pd 
import pandas as pd
import numpy as np
import time
df = pd.read_csv("url.csv",header=None)
df = df.drop([0],axis=1)
df.rename(columns={1:"urls"},inplace=True)
df = df.iloc[1:,:]
df.head()
lst = list(df['urls'])
lst = lst[:560]
def stripping_views(c):
    res=''
    for i in c.strip().split()[0].split(','):
        res = res+i
    return int(res)
views = list()
date = list()
likes = list()
dlikes =list()
comments = list()
comcount=list()
wasteurl = list()
l = 0
driver = webdriver.Firefox(executable_path=r'C:\Users\LOKSUNDAR\Dropbox\Kofluence project\geckodriver.exe')
for url in lst:
        driver.get(url)
        time.sleep(3)
        ele = driver.find_elements_by_class_name("style-scope ytd-video-primary-info-renderer")
        for vid in ele:
            view =vid.find_element_by_xpath('.//*[@id="count"]/yt-view-count-renderer/span[1]').text
            views.append(view)
            date.append(vid.find_element_by_xpath('.//*[@id="date"]/yt-formatted-string').text)
            lik = vid.find_elements_by_xpath('.//*[@id="text"]')
            likes.append(lik[0].text)
            dlikes.append(lik[1].text)
            driver.execute_script("window.scrollTo(0,720)")
            time.sleep(3)
            try :
                com = driver.find_elements_by_class_name('style-scope ytd-comment-renderer')[0].find_elements_by_xpath('//*[@id="content-text"]')
                co = list()
                for j in com:
                    co.append(j.text)
                comments.append(co)
                comcount.append(len(co))
            except:
                comments.append("no Comments ")
                comcount.append(0)
        l=l+1
        print(l,"links are completed out of ",len(lst))
        if (len(ele) == 0):
            wasteurl.append(url)
            print("this url:-",url," is not working")
for i in wasteurl:
    lst.remove(i)
nviws = [ stripping_views(i) for i in views]
df1 = pd.DataFrame()
df1['Vedio Urls'] = lst
df1['No of Views']=nviws
df1['Date Created']=date
df1['NO of Comments']=comcount
df1['comments']=comments
df1['Likes']=likes
df1['Dislikes']=dlikes
df1.to_csv("scrapdata.csv")